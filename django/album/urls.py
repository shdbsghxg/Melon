from . import views
from django.urls import path

app_name = 'album'
urlpatterns = [
    path('', views.album_list, name='album-list')
]
