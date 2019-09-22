from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    #  / home/
    url(r'^$', views.homeView, name='home'),
    url(r'^signup/$', views.signupView, name='signup'),

    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    path('profile/verify/<token>/', views.verify, name='profile-verify'),
    path('profile/', views.ProfileView, name='profile-view'),
]