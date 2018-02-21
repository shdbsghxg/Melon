# Generated by Django 2.0.2 on 2018-02-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0003_auto_20180208_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=30, null=True, verbose_name='아티스트'),
        ),
        migrations.AddField(
            model_name='song',
            name='song_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='melon Song ID'),
        ),
    ]
