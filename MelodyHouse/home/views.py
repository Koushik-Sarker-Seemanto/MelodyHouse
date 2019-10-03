
from django.shortcuts import redirect, render, HttpResponse



def homeView(request):
    if request.user.is_authenticated:
        return redirect('profile_app:profile-view')
    else:
        template = 'home/HomePage.html'
        return render(request, template)
