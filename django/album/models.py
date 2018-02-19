from django.db import models
from artist.models import Artist


class Album(models.Model):
    title = models.CharField('앨범명', max_length=50)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    release_date = models.DateField()

    @property
    def genre(self):
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        return '{title} [{artists}]'.format(
            title=self.title,
            artists=', '.join(self.artists.values_list('name', flat=True)),
        )

