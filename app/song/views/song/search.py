from typing import NamedTuple

from django.db.models import Q

from ...models import Song
from django.shortcuts import render

__all__ = (
    'song_search',
)


def song_search(request):
    """
    url : song/search/
    template : templates/song/song_search.html
        one input, button in form respectively
    :param request:
    :param title:
    :return:

    <GET/POST>
    1. input name = keyword
    2. two-ways : request.method = 'GET', 'POST'
    3. request.method == 'POST'
        return value of key 'keyword' by HttpResponse
    4. render 'song_search.html', itself

    <search by Query filter>
    1. make query_set of song. keyword included self.title
    2. query_set = songs
    3. context dict w/ 'songs':songs
    4. render including context
    5. print songs
    """
    # in case, keyword is included in name of Artist related with Song
    # in case, keyword is included in name of Album related with Song
    # in case, keyword is included in both( or --> Q object), 'songs' = queryset

    # <HW>
    # song_from_artists
    # song_from_albums
    # song_from_title
    # upper 3 variables --> querysets meeting higher conditions respectively
    # search_result show in 3 different ways
    # --> result by artist / album / song

    # when keyword is empty, how?? --> do sth, exception manage --> used get('keyword', None)

    context = {
        'song_infos': []
    }
    keyword = request.GET.get('keyword')

    class SongInfo(NamedTuple):
        type: str
        q: Q

    if keyword:
        song_infos = (
            SongInfo(type='artist', q=Q(album__artists__name__contains=keyword)),
            SongInfo(type='album', q=Q(album__title__contains=keyword)),
            SongInfo(type='title', q=Q(title__contains=keyword)),
        )
        for type, q in song_infos:
            context['song_infos'].append({
                'type': type,
                'songs': Song.objects.filter(q),
            })

            # context['song_infos'].append({
            #     'type': 'artist',
            #     'songs': song_from_artists,
            # })
            # context['song_infos'].append({
            #     'type': 'album',
            #     'songs': song_from_albums,
            # })
            # context['song_infos'].append({
            #     'type': 'title',
            #     'songs': song_from_title,
            # })
            # title__contains
            # songs = Song.objects.filter(
            #     Q(title__contains=keyword) |
            #     Q(album__title__contains=keyword) |
            #     Q(album__artists__name__contains=keyword)
            # ).distinct()

            # GET/POST two cases --> context empty/filled two cases
            # --> if / else trimmed
            # context['songs'] = songs

    return render(request, 'song/song_search.html', context)
