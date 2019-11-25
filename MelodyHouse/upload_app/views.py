from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from authentication.models import Account
from  profile_app.models import Post
from upload_app.models import Album, Song
from upload_app.forms import AlbumForm, SongForm

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/signin/')
def addAlbum(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user

            if album.album_logo in request.POST:
                album.album_logo = request.FILES['album_logo']
                file_type = album.album_logo.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    form = AlbumForm()
                    form_song = SongForm()
                    context = {
                        'form': form,
                        'form_song': form_song,
                        'error_message': 'Album Already Exists!!!',
                    }
                    return render(request, 'upload_app/uploadPage.html', context)

            artist = form.cleaned_data['artist']
            album_title = form.cleaned_data['album_title']
            query = Album.objects.filter(artist=artist).filter(album_title=album_title).filter(user=request.user)
            if query.exists():
                form = AlbumForm()
                form_song = SongForm()
                context = {
                    'form': form,
                    'form_song': form_song,
                    'error_message': 'Album Already Exists!!!',
                }
                return render(request, 'upload_app/uploadPage.html', context)
            else:
                album.save()
                post_instance = Post()
                post_instance.post_type = 'album'
                post_instance.post_album = album
                post_instance.post_user = request.user
                post_instance.save()
                return redirect('profile_app:profile-view')

        form_song = SongForm(request.POST, request.FILES)
        if form_song.is_valid():
            song = form_song.save(commit=False)
            song.user = request.user

            song.song_file = request.FILES['song_file']
            file_type = song.song_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                form = AlbumForm()
                form_song = SongForm()
                context = {
                    'form': form,
                    'form_song': form_song,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'upload_app/uploadPage.html', context)

            song_file = form_song.cleaned_data['song_file']
            album_id = form_song.cleaned_data['album_id']

            query = Song.objects.filter(album_id=album_id).filter(song_file=song_file)
            if query.exists():
                form = AlbumForm()
                form_song = SongForm()
                context = {
                    'form': form,
                    'form_song': form_song,
                    'error_message': 'Song Already Exists!!!',
                }
                return render(request, 'upload_app/uploadPage.html', context)
            else:
                song.save()
                post_instance = Post()
                post_instance.post_type = 'song'
                post_instance.post_song = song
                post_instance.post_user = request.user
                post_instance.save()
                return redirect('profile_app:profile-view')

    else:
        form = AlbumForm()
        form_song = SongForm()
    context = {
        'form': form,
        'form_song': form_song
    }
    return render(request, 'upload_app/uploadPage.html', context)
