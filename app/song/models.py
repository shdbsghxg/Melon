from datetime import datetime

import re

import requests
from bs4 import NavigableString, BeautifulSoup
from django.db import models

from album.models import Album
from artist.models import Artist


class SongManager(models.Manager):

    def update_or_create_from_melon(self, song_id):
        """
        Song info from melon w/ song_id
        Artist info from melon w/ artist_id, and ArtistManager.update_or_create_from_melon

        :param song_id:
        :return: Song instance, bool(song_created)
        """
        url = 'https://melon.com/song/detail.htm'
        params = {
            'songId': song_id,
        }

        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')

        div_entry = soup.find('div', class_='entry')

        artist_id_cont = div_entry.find('div', class_='info').select_one('div.artist > a.artist_name').get('href')
        artist_id = re.search(r'goArtistDetail\(\'(.*?)\'\)', artist_id_cont).group(1)
        album_id_cont = div_entry.find('div', class_='meta').select_one('dl.list > dd:nth-of-type(1) > a').get('href')
        album_id = re.search(r'goAlbumDetail\(\'(.*?)\'\)', album_id_cont).group(1)
        # print(f'-----{artist_id_cont}')
        # print(f'-----{artist_id}')
        # print(f'-----{album_id_cont}')
        # print(f'-----{album_id}')

        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
        artist = div_entry.find('div', class_='artist').get_text(strip=True)

        dl = div_entry.find('div', class_='meta').find('dl')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        it = iter(items)
        description_dict = dict(zip(it, it))

        # album must be an object
        # album = description_dict.get('앨범')
        # release_song_date_str = description_dict.get('발매일')
        # release_song_date = datetime.strptime(release_song_date_str, '%Y.%m.%d')
        genre = description_dict.get('장르')

        div_lyric = soup.find('div', id='d_video_summary')

        if div_lyric:
            lyrics_list = []
            for item in div_lyric:
                if item.name == 'br':
                    lyrics_list.append('\n')
                elif type(item) is NavigableString:
                    lyrics_list.append(item.strip())
            lyrics = ''.join(lyrics_list)

        artist, artist_created = Artist.objects.update_or_create_from_melon(artist_id)
        album, album_created = Album.objects.update_or_create_from_melon(album_id)
        song, song_created = self.update_or_create(
            melon_id=song_id,
            defaults={
                'title': title,
                # 'artist': artist,
                'album': album,
                # 'release_song_date': datetime.strftime(release_song_date, '%Y-%m-%d'),
                'genre': genre,
                'lyrics': lyrics,
                # 'artist_id': artist_id,
                # 'album_id': album_id,
            }
        )

        song.artists.add(artist)

        return song, song_created


class Song(models.Model):
    melon_id = models.CharField('melon Song ID', max_length=20, blank=True, null=True, unique=True)
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )
    title = models.CharField('곡 제목', max_length=100)
    genre = models.CharField('장르', max_length=100)
    lyrics = models.TextField('가사', blank=True)

    objects = SongManager()

    @property
    def release_date(self):
        # self.album - release_date
        return self.album.release_date

    @property
    def formatted_release_date(self):
        # ex) 2017.01.15
        return self.release_date.strftime('%Y.%m.%d')

    # def __str__(self):
    # if self.album:
    #     return '{artists} - {title} ({album})'.format(
    #         # artists=', '.join(self.album.artists.values_list('name', flat=True)),
    #         title=self.title,
    #         album=self.album.title,
    #     )

    def __str__(self):
        return '{artist} - {title}'.format(
            # artist=self.artists.name,
            artist=', '.join(self.artists.values_list('name', flat=True)),
            title=self.title,
            # album=self.album.title,
        )
