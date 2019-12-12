from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from generic.helper import decode as token_decode
from upload_app.models import Album, Song
from authentication.models import Account
from generic.service import verify_email
from profile_app.forms import ProfileUpdateForm
from django.db.models import Q
from friendship.models import Friend, Follow, Block, FriendshipRequest

@login_required(login_url='/signin/')
def SearchResult(request):
    search_key = request.GET.get('search_field')
    search_text = request.POST.get('search_text')
    print("Search_Key")
    print(search_key)
    print("Search Text")
    print(search_text)
    user = request.user
    albums = Album.objects.filter(album_title__icontains=search_key)
    USERS = Account.objects.filter(name__icontains=search_key).exclude(id=user.id)
    songs = Song.objects.filter(song_title__icontains=search_key)

    USERS = list(USERS)
    friends = []

    for usr in USERS:
        check_friend = Friend.objects.are_friends(request.user, usr)
        if check_friend == True:
            USERS.remove(usr)
            friends.append(usr)

    print(USERS)
    print(friends)

    context = {
        'user': user,
        'albums': albums,
        'USERS': USERS,
        'friends': friends,
        'songs': songs,
        'error_message': '',
    }

    if request.method == 'POST':

        if request.POST.get('search_btn') == "search_btn":
            user_field = request.POST.get('user_field', '') == 'on'
            album_field = request.POST.get('album_field', '') == 'on'
            song_field = request.POST.get('song_field', '') == 'on'
            # user_field = request.POST['user_field']
            # album_field = request.POST['album_field']
            # song_field = request.POST['song_field']
            search_text = request.POST['search_text']
            print(search_text)
            print(user_field)
            print(album_field)
            print(song_field)
            if request.POST.get('user_field', '') == 'on':
                print("looooooooooooopppppppppppp")
            user = request.user
            albums = Album.objects.filter(album_title__icontains=search_text)
            USERS = Account.objects.filter(name__icontains=search_text).exclude(id=user.id)
            songs = Song.objects.filter(song_title__icontains=search_text)
            USERS = list(USERS)
            friends = []
            for usr in USERS:
                check_friend = Friend.objects.are_friends(request.user, usr)
                if check_friend == True:
                    USERS.remove(usr)
                    friends.append(usr)

            if request.POST.get('user_field', '') == 'on' and request.POST.get('album_field', '') == 'on' and request.POST.get('song_field', '') == 'on':
                print("All keys are ON")

                context = {
                    'user': user,
                    'albums': albums,
                    'USERS': USERS,
                    'friends': friends,
                    'songs': songs,
                    'error_message': '',
                }
                return render(request, 'search_app/SearchPage.html', context)

            elif request.POST.get('user_field', '') == 'on':
                print("user is ON")
                songs = ''
                albums = ''
                context = {
                    'user': user,
                    'albums': '',
                    'USERS': USERS,
                    'friends': friends,
                    'songs': songs,
                    'error_message': albums,
                }
                return render(request, 'search_app/SearchPage.html', context)

            elif request.POST.get('album_field', '') == 'on':
                print("album is ON")
                context = {
                    'user': user,
                    'albums': albums,
                    'USERS': '',
                    'friends': '',
                    'songs': '',
                    'error_message': '',
                }
                return render(request, 'search_app/SearchPage.html', context)

            elif request.POST.get('song_field', '') == 'on':
                context = {
                    'user': user,
                    'albums': '',
                    'USERS': '',
                    'friends': '',
                    'songs': songs,
                    'error_message': '',
                }
                print("song is ON")
                return render(request, 'search_app/SearchPage.html', context)

        if request.POST.get('add_friend') == "send_request":
            user_id = request.POST['user_id']
            print(user_id)
            other_user = Account.objects.get(pk=user_id)
            Friend.objects.add_friend(
                request.user,  # The sender
                other_user,  # The recipient
                message='Hi! I would like to add you')
            context = {
                'user': user,
                'albums': albums,
                'USERS': USERS,
                'friends': friends,
                'songs': songs,
                'error_message': 'Friend Request Sent!!!',
            }
            return render(request, 'search_app/SearchPage.html', context)

    return render(request, 'search_app/SearchPage.html', context)
