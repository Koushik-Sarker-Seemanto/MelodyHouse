from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from upload_app.models import Album, Song
from profile_app.models import Post,PlayList
from authentication.models import Account
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm
from friendship.models import Friend, FriendshipRequest
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
        print("Chhhhhhhhhhhhhhhecccccccccccccckkkkkkkkkkkkkkk")

        print(song_id)
        song = PlayList.objects.get(id=song_id)

        temp_check = Post.objects.get(post_song_id=song.playlist_song_id)
        temp_check.check_playlist = "0"
        temp_check.save()


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
    print("Innnnnnniiiiiiiiiiiiiiiiiittttttttttttttttttttttttttttt")
    user = request.user
    albums = Album.objects.all()
    side_albums = albums.all().order_by('-date_time')[:4]
    side_albums = list(side_albums)

    myFriend = Friend.objects.friends(user)
    myFriend = list(myFriend)

    mylist = PlayList.objects.filter(playlist_user=request.user)
    mylist = list(mylist)

    allpost = Post.objects.all()
    allpost = allpost.all().order_by("-date_time")
    allpost = list(allpost)

    for item in allpost:
        temp_post = item.post_song_id
        for myitem in mylist:
            temp_list = myitem.playlist_song_id
            if temp_post == temp_list:
                item.check_playlist = "1"
                item.save()
                break
            elif temp_post != temp_list:
                item.check_playlist = "0"
                item.save()

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

    friends_album = list()

    for temp in post:
        if temp.post_type == "album":
            friends_album.append(temp)

    friends_album = friends_album[0:6]

    if request.POST.get('add_to_playlist') == "add_to_playlist":
        print("Add button clickedddddddddddddddddddddddddddddddddddddddd")
        song_id = request.POST['song_id']
        print(song_id)

        temp_check = Post.objects.get(post_song_id=song_id)
        temp_check.check_playlist = "1"
        temp_check.save()
        print("DATA savedddddddddddddddddddddddd toooooooooooooooo DDDDDDDDDBBBBB")
        print(temp_check.check_playlist)

        song = Song.objects.get(id=song_id)
        song_exist = PlayList.objects.filter(playlist_song=song).filter(playlist_user=request.user)

        if song_exist.exists():
            context = {
                "friends_album": friends_album,
                "error": "Already in Playlist",
                'side_albums': side_albums,
                'post': post,
                'user': user
            }
            return redirect('profile_app:news-feed')
            # return render(request, 'profile_app/NewsFeed.html', context)
        else:
            playlist_instance = PlayList()
            playlist_instance.playlist_song = song
            playlist_instance.playlist_user = request.user
            playlist_instance.save()

            context = {
                "friends_album": friends_album,
                "error": "Added to Playlist",
                'side_albums': side_albums,
                'post': post,
                'user': user
            }
            return render(request, 'profile_app/NewsFeed.html', context)

    print(post)
    context = {
        "friends_album": friends_album,
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
    check_friend = Friend.objects.are_friends(request.user, view_user)
    friend_checking = "x"

    if check_friend == True:
        friend_checking = "1"
    else:
        friend_checking = "0"

    sent_request = FriendshipRequest.objects.filter(from_user=request.user).filter(to_user=view_user)
    if sent_request:
        friend_checking = "pending"

    post = Post.objects.filter(post_user=view_user)
    post = post.all().order_by('-date_time')

    albums = Album.objects.filter(user=view_user)
    side_albums = albums.all().order_by('-date_time')[:4]

    if request.POST.get('add_friend') == "add_friend":
        user_id = request.POST['user_id']
        print(user_id)
        other_user = Account.objects.get(pk=user_id)
        Friend.objects.add_friend(
            request.user,  # The sender
            other_user,  # The recipient
            message='Hi! I would like to add you')
        sent_request = FriendshipRequest.objects.filter(from_user=request.user).filter(to_user=view_user)
        if sent_request:
            friend_checking = "pending"

        context = {
            "friend_checking": friend_checking,
            "post": post,
            "side_albums": side_albums,
            "view_user": view_user,
            "user": user,
            "error": "Friend request sent!!!"
        }
        return render(request, 'profile_app/peopleProfile.html', context)
    if request.POST.get('un_friend') == "un_friend":
        user_id = request.POST['user_id']
        print(user_id)
        other_user = Account.objects.get(pk=user_id)
        Friend.objects.remove_friend(request.user, other_user)
        context = {
            "friend_checking": friend_checking,
            "post": post,
            "side_albums": side_albums,
            "view_user": view_user,
            "user": user,
            "error": "Un-friend user!!!"
        }
        return render(request, 'profile_app/peopleProfile.html', context)

    context = {
        "friend_checking": friend_checking,
        "post": post,
        "side_albums": side_albums,
        "view_user": view_user,
        "user": user,
        "error": "",
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
    albums = Album.objects.filter(user=request.user)[0:6]
    songs = Song.objects.filter(user=request.user).filter(album_id=current_album)

    context = {
        'current_album': current_album,
        'songs': songs,
        'albums': albums,
        'user': user,
    }
    return render(request, 'profile_app/MyUploads.html', context)


@login_required(login_url='/signin/')
def MyUploadsSongRemove(request, pk):
    removed_song = Song.objects.get(id=pk)
    print(removed_song.song_title, removed_song.id)

    playlist_remove = PlayList.objects.filter(playlist_song=removed_song)
    post_remove = Post.objects.filter(post_song=removed_song)
    print(playlist_remove)
    print(post_remove)

    post_remove.delete()
    playlist_remove.delete()
    removed_song.delete()

    user = request.user
    albums = Album.objects.filter(user=request.user)
    songs = Song.objects.filter(user=request.user)

    context = {
        'songs': songs,
        'albums': albums,
        'user': user,
    }
    # return redirect('profile_app:my_album_songs', context)
    return render(request, 'profile_app/MyUploads.html', context)


@login_required(login_url='/signin/')
def MyUploadsAlbumRemove(request, pk):
    removed_album = Album.objects.get(id=pk)
    print(removed_album.album_title, removed_album.id)

    if removed_album.user_id == request.user:
        removed_album.delete()
    else:
        error = "  This is not your album"

    user = request.user
    albums = Album.objects.filter(user=request.user)
    songs = Song.objects.filter(user=request.user)

    context = {
        'error': error,
        'songs': songs,
        'albums': albums,
        'user': user,
    }
    return render(request, 'profile_app/MyUploads.html', context)


@login_required(login_url='/signin/')
def SingleAlbum(request, pk):
    user = request.user
    album = Album.objects.get(id=pk)
    songs = Song.objects.filter(album_id=album)

    context = {
        'songs': songs,
        'albums': album,
        'user': user,
    }
    return render(request, 'profile_app/SingleAlbum.html', context)
