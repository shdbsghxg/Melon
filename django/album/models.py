from django.db import models
from artist.models import Artist


class Album(models.Model):
    title = models.CharField('앨범명', max_length=50)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    artists = models.ManyToManyField(Artist, verbose_name='artist list')
    release_date = models.DateField()

    @property
    def genre(self):
        return ''

    def __str__(self):
        return f'{title} [{artists}]'.format(
            title=self.title,
            artists=', '.join(self.artists.values_list('name', flat=True))
        )

