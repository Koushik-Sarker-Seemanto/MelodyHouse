from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'friends'

urlpatterns = [

    path('friends/', views.ViewFriends, name='ViewFriends'),
    path('requests/', views.viewRequest, name='view-request'),
    # path('addfriends/', views.friendship_add_friend, name='addfriends'),
    # path('acceptfriends/', views.friendship_accept, name='requestlist'),
    # path('requestlist/', views.friendship_request_list, name='requestlist'),

]