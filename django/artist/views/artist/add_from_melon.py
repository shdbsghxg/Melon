from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect

from crawler.artist import ArtistData
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
        # crawling part
        artist = ArtistData(artist_id)
        artist.get_detail()

        name = artist.name
        real_name = artist.personal_information.get('본명', '')
        nationality = artist.personal_information.get('국적', '')
        birth_date_str = artist.personal_information.get('생일', '')
        constellation = artist.personal_information.get('별자리', '')
        blood_type = artist.personal_information.get('혈액형', '')

        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
        else:
            blood_type = Artist.BLOOD_TYPE_OTHER

        # if artist w/ melon_id = artist_id already exists,
        # update date in DB,
        # or add new artist in DB
        Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d'),
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )
        return redirect('artist:artist-list')
