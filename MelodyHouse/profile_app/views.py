from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm


@login_required(login_url='/signin/')
def ProfileView(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile_app/profileView.html', context)


@login_required(login_url='/signin/')
def ProfileUpdate(request):
    context = {}
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=user)
        if form.is_valid():
            if form.is_new_email():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                verify_email(request, user)
                return HttpResponse('<h1 align="center">Verify Your Email. Check Your Mailbox</h1>')
            form.save()
            return redirect('/profile/')
    else:
        form = ProfileUpdateForm(user=request.user)

    context['form'] = form
    return render(request, 'profile_app/ProfileUpdate.html', context)
