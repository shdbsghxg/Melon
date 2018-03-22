from datetime import datetime

from django.core.files import File
from django.db import models

from crawler.artist import ArtistData
from utils.file import download, get_buffer_ext


class ArtistManager(models.Manager):

    def update_or_create_from_melon(self, artist_id):
        artist = ArtistData(artist_id)
        artist.get_detail()

        name = artist.name
        url_img_cover = artist.url_img_cover
        print(url_img_cover)
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
        artist, artist_created = self.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d') if birth_date_str else None,
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )

        temp_file = download(url_img_cover)
        file_name = '{artist_id}.{ext}'.format(
            artist_id=artist_id,
            ext=get_buffer_ext(temp_file),
        )

        if artist.img_profile:
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))

        return artist, artist_created


class Artist(models.Model):
    BLOOD_TYPE_A = 'A'
    BLOOD_TYPE_B = 'B'
    BLOOD_TYPE_AB = 'C'
    BLOOD_TYPE_O = 'O'
    BLOOD_TYPE_OTHER = 'X'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )

    melon_id = models.CharField('melon Artist ID', max_length=20, blank=True, null=True, unique=True)
    img_profile = models.ImageField('프로필 이미지', upload_to='artist', blank=True)
    name = models.CharField('이름', max_length=50)
    real_name = models.CharField('본명', max_length=30, blank=True)
    nationality = models.CharField('국적', max_length=50)
    # group -> no birth_date -> fix !
    birth_date = models.DateField('생년월일', blank=True, null=True)
    constellation = models.CharField('별자리', max_length=30)
    blood_type = models.CharField('혈액형', max_length=1, choices=CHOICES_BLOOD_TYPE, blank=True)
    intro = models.TextField('소개', blank=True)

    objects = ArtistManager()

    def __str__(self):
        return self.name
