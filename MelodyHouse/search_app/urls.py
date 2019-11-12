from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'search_app'

urlpatterns = [

    path('searchresults/', views.SearchResult, name='search-result'),

]