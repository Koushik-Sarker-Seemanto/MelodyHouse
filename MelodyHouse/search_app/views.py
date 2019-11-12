from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from upload_app.models import Album, Song
from authentication.models import Account
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm
from django.db.models import Q


@login_required(login_url='/signin/')
def SearchResult(request):
    # user = request.user
    # albums = Album.objects.all()
    # USERS = Account.objects.all()
    # songs = Song.objects.all()
    # context = {
    #     'user': user,
    #     'albums': albums,
    #     'USERS': USERS,
    #     'songs': songs,
    # }
    #
    search_key = request.GET.get('search_field')

    # search_key = request.POST['search_field']
    print(search_key)
    user = request.user
    albums = Album.objects.filter(album_title__icontains=search_key)
    USERS = Account.objects.filter(name__icontains=search_key)
    songs = Song.objects.filter(song_title__icontains=search_key)
    context = {
        'search_key': search_key,
        'user': user,
        'albums': albums,
        'USERS': USERS,
        'songs': songs,
    }

    return render(request, 'search_app/SearchPage.html', context)

