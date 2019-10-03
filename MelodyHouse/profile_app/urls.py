from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'profile_app'

urlpatterns = [

    path('profile/', views.ProfileView, name='profile-view'),
    path('update/',views.ProfileUpdate, name='profile-update'),

]