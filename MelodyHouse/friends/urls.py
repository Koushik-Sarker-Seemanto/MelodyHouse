from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'friends'

urlpatterns = [

    path('friends/', views.ViewFriends, name='ViewFriends'),

]