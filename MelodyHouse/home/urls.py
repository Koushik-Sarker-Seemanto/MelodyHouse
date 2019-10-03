from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    #  / home/
    url(r'^$', views.homeView, name='home'),

    path('profile/', views.ProfileView, name='profile-view'),
]