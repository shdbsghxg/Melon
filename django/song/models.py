from django.db import models

from album.models import Album


class Song(models.Model):
    song_id = models.CharField('melon Song ID', max_length=20, blank=True, null=True, unique=True)
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
    artist = models.CharField('아티스트', max_length=50, null=True)
    release_song_date = models.DateField(blank=True, null=True)

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

    # def __str__(self):
    #     return '{artists} - {title} ({album})'.format(
    #         # artists=', '.join(self.album.artists.values_list('name', flat=True)),
    #         title=self.title,
    #         album=self.album.title,
    #     )

    def __str__(self):
        return '{artist} - {title}'.format(
            artist=self.artist,
            title=self.title,
            # album=self.album,
        )
