from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from upload_app.models import Album, Song
from profile_app.models import Post,PlayList
from authentication.models import Account
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm
from friendship.models import Friend
from django.db.models import Q


@login_required(login_url='/signin/')
def ProfileView(request):
    user = request.user
    post = Post.objects.filter(post_user=user)
    post = post.all().order_by('-date_time')
    print(post)

    albums = Album.objects.filter(user=request.user)
    side_albums = albums.all().order_by('-date_time')[:4]
    albums = albums.all().order_by('-date_time')
    context = {
        'post': post,
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
    songs = PlayList.objects.filter(playlist_user=user)

    if request.POST.get('remove_from_playlist') == "remove_from_playlist":
        song_id = request.POST['song_id']
        song = PlayList.objects.get(id=song_id)
        song.delete()

        context = {
            'error': song.playlist_song.song_title + " has been removed from your playlist",
            'songs': songs,
            'user': user
        }
        return render(request, 'profile_app/PlayList.html', context)

    context = {
        'error': '',
        'songs': songs,
        'user': user
    }
    return render(request, 'profile_app/PlayList.html', context)


@login_required(login_url='/signin/')
def NewsFeedView(request):
    user = request.user
    albums = Album.objects.all()
    side_albums = albums.all().order_by('-date_time')[:3]
    side_albums = list(side_albums)

    myFriend = Friend.objects.friends(user)
    myFriend = list(myFriend)

    if myFriend:
        result = Post.objects.all()
        result_elms = []
        for frnd in myFriend:
            result_elms.append(result.filter(post_user=frnd))
        post = result_elms[0].union(*result_elms[1:])
        post = post.all().order_by("-date_time")
    else:
        post = Post.objects.all()
        post = post.all().order_by("-date_time")

    if request.POST.get('add_to_playlist') == "add_to_playlist":
        song_id = request.POST['song_id']
        print(song_id)

        song = Song.objects.get(id=song_id)
        song_exist = PlayList.objects.filter(playlist_song=song).filter(playlist_user=request.user)

        if song_exist.exists():
            context = {
                "error": "Already in Playlist",
                'side_albums': side_albums,
                'post': post,
                'user': user
            }
            return render(request, 'profile_app/NewsFeed.html', context)
        else:
            playlist_instance = PlayList()
            playlist_instance.playlist_song = song
            playlist_instance.playlist_user = request.user
            playlist_instance.save()

            context = {
                "error": "Added to Playlist",
                'side_albums': side_albums,
                'post': post,
                'user': user
            }
            return render(request, 'profile_app/NewsFeed.html', context)

    print(post)
    context = {
        "error": "",
        'side_albums': side_albums,
        'post': post,
        'user': user
    }

    return render(request, 'profile_app/NewsFeed.html', context)


@login_required(login_url='/signin/')
def PeopleProfile(request, pk):
    user = request.user
    view_user = Account.objects.get(id=pk)
    print(view_user)

    post = Post.objects.filter(post_user=view_user)
    post = post.all().order_by('-date_time')

    albums = Album.objects.filter(user=view_user)
    side_albums = albums.all().order_by('-date_time')[:4]

    context = {
        "post": post,
        "side_albums": side_albums,
        "view_user": view_user,
        "user": user,
    }
    return render(request, 'profile_app/peopleProfile.html', context)


@login_required(login_url='/signin/')
def MyUploads(request):
    user = request.user
    albums = Album.objects.filter(user=request.user)
    songs = Song.objects.filter(user=request.user)

    context = {
        'songs': songs,
        'albums': albums,
        'user': user,
    }
    return render(request, 'profile_app/MyUploads.html', context)


@login_required(login_url='/signin/')
def MyUploadedAlbum(request, pk):
    user = request.user
    current_album = Album.objects.get(id=pk)
    albums = Album.objects.filter(user=request.user)
    songs = Song.objects.filter(user=request.user).filter(album_id=current_album)

    context = {
        'current_album': current_album,
        'songs': songs,
        'albums': albums,
        'user': user,
    }
    return render(request, 'profile_app/MyUploads.html', context)
