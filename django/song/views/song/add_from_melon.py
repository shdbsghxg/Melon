from datetime import datetime

import requests
from bs4 import BeautifulSoup, NavigableString
from django.http import HttpResponse
from django.shortcuts import redirect

from ...models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        # crawl
        url = 'https://melon.com/song/detail.htm'
        params = {
            'songId': song_id,
        }

        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')

        div_entry = soup.find('div', class_='entry')

        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
        artist = div_entry.find('div', class_='artist').get_text(strip=True)

        dl = div_entry.find('div', class_='meta').find('dl')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        it = iter(items)
        description_dict = dict(zip(it, it))

        album = description_dict.get('앨범')
        release_song_date_str = description_dict.get('발매일')
        release_song_date = datetime.strptime(release_song_date_str, '%Y.%m.%d')
        genre = description_dict.get('장르')

        div_lyric = soup.find('div', id='d_video_summary')

        lyrics_list = []
        for item in div_lyric:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())
        lyrics = ''.join(lyrics_list)

        song, _ = Song.objects.update_or_create(
            song_id=song_id,
            defaults={
                'title': title,
                'artist': artist,
                # 'album': album,
                'release_song_date': datetime.strftime(release_song_date, '%Y-%m-%d'),
                'genre': genre,
                'lyrics': lyrics,
            }
        )
        return redirect('song:song-list')
