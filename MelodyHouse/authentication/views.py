from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from authentication.models import Account
from authentication.forms import SignupForm, SigninForm, PasswordChangeForm


def signupView(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            verify_email(request, user)
            return HttpResponse('<h1 align="center">Verify Your Email. Check Your Mailbox</h1>')

    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'authentication/signup.html', context)


def verify(request, token):
    data = token_decode(token)
    if data is None:
        return views.invalid_request(request)

    user_id = data['user_id']
    email = data['email']

    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    login(request, user)
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile/../profile_app/templates/profile_app/profileView.html', context)
    # return HttpResponse('<h1 align="center">Email verified</h1>')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
            return redirect('home:profile-view')
    else:
        form = SigninForm()
        print(form.as_table())
        context = {
            'form': form
        }
        return render(request, 'authentication/signin.html', context)


@login_required(login_url='/signin/')
def signout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/signin/')
def change_password(request):
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            logout(request)
            login(request, user)

            return redirect('/profile/')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form

    return render(request, 'authentication/PasswordChange.html', context)
