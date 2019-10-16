from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from authentication.models import Account
from upload_app.models import Album, Song
from upload_app.forms import AlbumForm, SongForm


@login_required(login_url='/signin/')
def addAlbum(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user

            artist = form.cleaned_data['artist']
            album_title = form.cleaned_data['album_title']
            query = Album.objects.filter(artist=artist).filter(album_title=album_title).filter(user=request.user)
            if query.exists():
                return HttpResponse('<h1 align="center" style="color: red;margin-top: 400px">Album Already Exists!!!</h1>')
            else:
                album.save()
                return redirect('profile_app:profile-view')

        form_song = SongForm(request.POST, request.FILES)
        if form_song.is_valid():
            song = form_song.save(commit=False)

            song_file = form_song.cleaned_data['song_file']
            album_id = form_song.cleaned_data['album_id']

            query = Song.objects.filter(album_id=album_id).filter(song_file=song_file)
            if query.exists():
                return HttpResponse(
                    '<h1 align="center" style="color: red;margin-top: 400px">Song Already Exists!!!</h1>')
            else:
                song.save()
                return redirect('profile_app:profile-view')

    else:
        form = AlbumForm()
        form_song = SongForm()
    context = {
        'form': form,
        'form_song': form_song
    }
    return render(request, 'upload_app/uploadPage.html', context)
