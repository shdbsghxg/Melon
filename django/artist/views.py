from django.shortcuts import render

from artist.models import Artist


def artist_list(request):
    # show artist ist ad ul > li
    # use template 'artist/artist_list.html'
    # 'artists' for context to be delivered
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(request, 'artist/artist_list.html', context)
