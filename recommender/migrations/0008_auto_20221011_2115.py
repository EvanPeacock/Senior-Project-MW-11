# Generated by Django 3.2.15 on 2022-10-12 01:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommender', '0007_auto_20221011_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='playlist_owner',
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_owner',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
