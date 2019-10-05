from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from generic.service import verify_email
from authentication.models import Account
from upload_app.models import Album
from upload_app.forms import AlbumForm


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
                raise form.ValidationError('invalid password')
            else:
                album.save()
                return redirect('profile_app:profile-view')

    else:
        form = AlbumForm()
    context = {
        'form': form
    }
    return render(request, 'upload_app/uploadPage.html', context)
