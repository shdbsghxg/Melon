from django.shortcuts import render

from album.models import Album


def album_list(request):
    # show artist ist ad ul > li
    # use template 'artist/artist_list.html'
    # 'artists' for context to be delivered
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'album/album_list.html', context)
