from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from authentication.models import Account
from authentication.forms import SignupForm, SigninForm


def homeView(request):
    template = 'home/HomePage.html'
    return render(request, template)

