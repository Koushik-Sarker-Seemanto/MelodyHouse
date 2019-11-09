from django.shortcuts import render,redirect,get_object_or_404
from authentication.models import Account
from django.contrib.auth.decorators import login_required
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, Block, FriendshipRequest


@login_required(login_url='/signin/')
def ViewFriends(request):
    template = 'friends/viewfriendsPage.html'
    user = request.user
    peoples = Account.objects.exclude(id=request.user.id)

    context = {
        'user': user,
        'peoples': peoples,
        'error_message': '',
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        print(user_id)
        other_user = Account.objects.get(pk=user_id)
        Friend.objects.add_friend(
            request.user,  # The sender
            other_user,  # The recipient
            message='Hi! I would like to add you')
        context = {
            'user': user,
            'peoples': peoples,
            'error_message': 'Friend Request Sent!!!',
        }

    return render(request, template, context)


# @login_required('/signin/')
# def addFrined(request):
#     if request.method == 'POST':
#         user_id = request.POST['user_id']
#         other_user = Account.objects.get(pk=user_id)
#         Friend.objects.add_friend(
#             request.user,  # The sender
#             other_user,  # The recipient
#             message='Hi! I would like to add you')
#

#
# @login_required
# def friendship_add_friend(
#     request, to_user, template_name="friends/add.html"
# ):
#     """ Create a FriendshipRequest """
#     ctx = {"to_user": to_user}
#
#     if request.method == "POST":
#         to_user = Account.objects.get(user=to_user)
#         from_user = request.user
#         try:
#             Friend.objects.add_friend(from_user, to_user)
#         except AlreadyExistsError as e:
#             ctx["errors"] = ["%s" % e]
#         else:
#             return redirect("friendship_request_list")
#
#     return render(request, template_name, ctx)












































