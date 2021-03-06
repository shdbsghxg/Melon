from datetime import datetime

from bs4 import BeautifulSoup
from django.core.files import File
from django.db import models
import requests

from utils.file import download, get_buffer_ext


class AlbumManager(models.Manager):

    def update_or_create_from_melon(self, album_id):
        # crawl
        url = 'https://www.melon.com/album/detail.htm'
        params = {
            'albumId': album_id,
        }

        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')

        url_img_cover_cont = soup.find('div', class_='thumb')
        info_cont = soup.find('div', class_='entry')

        # rsplit( separator, number of splits ) --> list
        url_img_cover = url_img_cover_cont.select_one('a.image_typeAll > img').get('src').rsplit('?', 1)[0]
        print(url_img_cover)
        title = info_cont.select_one('div.info > div.song_name strong').next_sibling.strip()
        release_date = info_cont.select_one('div.meta > dl.list > dd:nth-of-type(1)').text

        album, album_created = self.update_or_create(
            melon_id=album_id,
            defaults={
                'title': title,
                'release_date': datetime.strptime(release_date, '%Y.%m.%d')
            }
        )

        temp_file = download(url_img_cover)
        file_name = '{album_id}.{ext}'.format(
            album_id=album_id,
            ext=get_buffer_ext(temp_file),
        )
        # saving an img in a row creates new img file
        # why??
        if album.img_cover:
            album.img_cover.delete()
        album.img_cover.save(file_name, File(temp_file))

        return album, album_created


class Album(models.Model):
    melon_id = models.CharField('melon Album ID', max_length=20, blank=True, null=True, unique=True)

    title = models.CharField('앨범명', max_length=50)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    release_date = models.DateField(blank=True, null=True)

    objects = AlbumManager()

    @property
    def genre(self):
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        # return '{title} [{artists}]'.format(
        #     title=self.title,
        #     artists=', '.join(self.artists.values_list('name', flat=True)),
        # )
        return self.title
