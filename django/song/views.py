from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from song.models import Song

from django.db.models import Q


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs
    }
    return render(request, 'song/song_list.html', context)


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
    context = {}
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

    if request.method == 'POST':
        # when keyword is empty, no queryset return
        keyword = request.POST['keyword'].strip()
        if keyword:
            # song_from_artists
            song_from_artists = Song.objects.filter(
                album__artists__name__contains=keyword
            )
            context['songs_from_artists'] = song_from_artists
            # song_from_albums
            song_from_albums = Song.objects.filter(
                album__title__contains=keyword
            )
            context['songs_from_albums'] = song_from_albums
            # song_from_title
            song_from_title = Song.objects.filter(
                title__contains=keyword
            )
            context['songs_from_title'] = song_from_title
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
