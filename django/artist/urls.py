from . import views
from django.urls import path

app_name = 'artist'
urlpatterns = [
    path('', views.artist_list, name='artist-list')
]