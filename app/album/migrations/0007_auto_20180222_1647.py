# Generated by Django 2.0.2 on 2018-02-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0006_album_melon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
