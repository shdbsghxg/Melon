from django.shortcuts import render

from ...models import Artist

__all__ = (
    'artist_list',
)


def artist_list(request):
    # show artist ist ad ul > li
    # use template 'artist/artist_list.html'
    # 'artists' for context to be delivered
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(request, 'artist/artist_list.html', context)
