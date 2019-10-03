from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    #  / home/
    url(r'^signup/$', views.signupView, name='signup'),

    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/verify/<token>/', views.verify, name='profile-verify'),
]


