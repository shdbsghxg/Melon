# Generated by Django 2.0.2 on 2018-02-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0007_auto_20180222_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='melon_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='melon Album ID'),
        ),
    ]