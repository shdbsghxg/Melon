
from django.shortcuts import redirect
from ...models import Artist

__all__ = (
    'artist_add_from_melon',
)


def artist_add_from_melon(request):
    """
    1. artist_search_from_melon.html -> new form w/ POST method

    2. get form-POST
        request.POST['artist_id']

        w/ artist_id, crawl artist_detail from melon
        name
        real_name
        etc...



        1) show w/ HttpResponse
        2) make Artist object, save to DB
        3) redirect artist:artist-list
    :param request:
    :return:
    """

    if request.method == 'POST':
        artist_id = request.POST['artist_id']
        Artist.objects.update_or_create_from_melon(artist_id)

        return redirect('artist:artist-list')
