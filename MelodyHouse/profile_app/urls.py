from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'profile_app'

urlpatterns = [

    path('newsfeed/', views.NewsFeedView, name='news-feed'),
    path('profile/', views.ProfileView, name='profile-view'),
    path('update/', views.ProfileUpdate, name='profile-update'),
    path('playlist/', views.Playlist, name='playlist'),
    path('people/<int:pk>/', views.PeopleProfile, name='people-profile'),
    path('myuploads/', views.MyUploads, name='my_uploads'),
    path('myuploads/<int:pk>/', views.MyUploadedAlbum, name='my_album_songs'),

]