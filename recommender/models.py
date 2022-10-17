from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models  
from django.contrib.auth.models import User

class Musicdata(models.Model):
    track_id = models.TextField()
    track_name = models.TextField()
    track_artist = models.TextField()
    track_popularity  = models.FloatField()
    track_album_id  = models.TextField()
    track_album_name = models.TextField()
    track_album_release_date = models.IntegerField()
    # playlist_name = models.TextField()
    # playlist_id = models.TextField()
    # playlist_genre = models.TextField()
    # playlist_subgenre = models.TextField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    
class Playlist(models.Model):
    playlist_name = models.CharField(max_length=50, null=False, blank=False, default='New Playlist')
    playlist_id = models.IntegerField(unique=True, null=False)
    playlist_owner = models.ManyToManyField(User, blank=True)
    playlist_songs = models.ManyToManyField('Musicdata', blank=True)
    
    def creator(self):
        return str(self.playlist_owner.all())