from django.shortcuts import render
from authentication.models import Account
from django.contrib.auth.decorators import login_required


@login_required(login_url='/signin/')
def ViewFriends(request):
    template = 'friends/viewfriendsPage.html'
    user = request.user
    peoples = Account.objects.all()
    context = {
        'user': user,
        'peoples': peoples,
    }

    return render(request, template, context)
