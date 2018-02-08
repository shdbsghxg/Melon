from . import views
from django.urls import path

app_name = 'song'
urlpatterns = [
    path('', views.song_list, name='song-list')
]
