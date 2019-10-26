from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from upload_app.models import Album, Song
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm
from django.db.models import Q


@login_required(login_url='/signin/')
def ProfileView(request):
    user = request.user
    albums = Album.objects.filter(user=request.user)
    side_albums = albums.all().order_by('-date_time')[:4]
    albums = albums.all().order_by('-date_time')
    context = {
        'side_albums': side_albums,
        'albums': albums,
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


@login_required(login_url='/signin/')
def Playlist(request):
    user = request.user
    # albums = Album.objects.filter(user=request.user)
    # for album in albums:
    #     album = Album.objects.get(user=request.user)
    #     songs = Song.objects.filter(album_id=album)
    songs = Song.objects.filter(user=user).order_by('-date_time')
    print(songs)
    context = {
        'songs': songs,
        'user': user
    }
    return render(request, 'profile_app/PlayList.html', context)
