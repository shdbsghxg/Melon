# Generated by Django 2.0.2 on 2018-02-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='melon_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='melon Artist ID'),
        ),
    ]
