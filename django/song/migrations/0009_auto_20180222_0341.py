# Generated by Django 2.0.2 on 2018-02-22 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0008_auto_20180222_0303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='song_id',
            new_name='melon_id',
        ),
    ]
