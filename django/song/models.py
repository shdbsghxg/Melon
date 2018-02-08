from django.db import models

from album.models import Album


class Song(models.Model):
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.CharField('곡 제목', max_length=100)
    genre = models.CharField('장르', max_length=100)
    lyrics = models.TextField('가사', blank=True)

    @property
    def artists(self):
        # self.album - Artists Queryset
        return self.album.artists.all()

    @property
    def release_date(self):
        # self.album - release_date
        return self.album.release_date

    @property
    def formatted_release_date(self):
        # ex) 2017.01.15
        return self.release_date.strftime('%Y.%m.%d')

    def __str__(self):
        return '{artists} - {title} ({album})'.format(
            artists=', '.join(self.album.artists.values_list('name', flat=True)),
            title=self.title,
            album=self.album.title,
        )
