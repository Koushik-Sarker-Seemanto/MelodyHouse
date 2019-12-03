from django.shortcuts import render,redirect,get_object_or_404
from authentication.models import Account
from django.contrib.auth.decorators import login_required
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, Block, FriendshipRequest


@login_required(login_url='/signin/')
def ViewFriends(request):
    template = 'friends/viewfriendsPage.html'
    user = request.user
    peoples = Friend.objects.friends(user)
    friendship_requests = Friend.objects.unrejected_requests(user)
    print(peoples)
    print(friendship_requests)

    context = {
        'user': user,
        'peoples': peoples,
        "requests": friendship_requests,
        'error_message': '',
    }

    if request.method == 'POST':

        if request.POST.get('action') == "accept":
            user = request.user
            friendship_request_id = request.POST['friendship_request_id']
            friend_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            friend_request.accept()

            peoples = Friend.objects.friends(user)
            friendship_requests = Friend.objects.unrejected_requests(user=request.user)
            context = {
                'user': user,
                'peoples': peoples,
                "requests": friendship_requests,
                'error_message': ' Friend Request Accepted!!!',
            }

        elif request.POST.get('action') == "reject":
            user = request.user
            friendship_request_id = request.POST['friendship_request_id']
            friend_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            friend_request.reject()

            peoples = Friend.objects.friends(user)
            friendship_requests = Friend.objects.unrejected_requests(user=request.user)
            context = {
                'user': user,
                'peoples': peoples,
                "requests": friendship_requests,
                'error_message': ' Friend Request Rejected!!!',
            }

        if request.POST.get('unfriend') == 'unfriend_request':
            user_id = request.POST['user_id']
            print(user_id)
            other_user = Account.objects.get(pk=user_id)
            Friend.objects.remove_friend(request.user, other_user)

            friendship_requests = Friend.objects.unrejected_requests(user=request.user)
            peoples = Friend.objects.friends(user)
            context = {
                'user': user,
                'peoples': peoples,
                'friend_requests': friendship_requests,
                'error_message': ' Unfriend done!!!',
            }

    return render(request, template, context)


@login_required(login_url='/signin/')
def viewRequest(request):
    template = 'friends/FriendRequestList.html'
    user = request.user
    friendship_requests = Friend.objects.unrejected_requests(user=request.user)
    context = {
        'user': user,
        "requests": friendship_requests,
        'error_message': '',
    }

    if request.method == 'POST':
        user = request.user
        friendship_request_id = request.POST['friendship_request_id']
        if request.POST['action'] == "accept":
            friend_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            friend_request.accept()
            friendship_requests = Friend.objects.unrejected_requests(user=request.user)
            context = {
                'user': user,
                "requests": friendship_requests,
                'error_message': 'Friend Request Accepted!!!',
            }

        elif request.POST['action'] == "reject":

            friend_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            friend_request.reject()
            friendship_requests = Friend.objects.unrejected_requests(user=request.user)
            context = {
                'user': user,
                "requests": friendship_requests,
                'error_message': 'Friend Request Rejected!!!',
            }

    return render(request, template, context)











































