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
    playlist_name = models.TextField()
    playlist_id = models.TextField()
    playlist_genre = models.TextField()
    playlist_subgenre = models.TextField()
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

class DislikedMusic(models.Model):
    user = models.ManyToManyField(User, null = True, blank = True)
    music = models.ManyToManyField(Musicdata,null = True, blank = True)

    
# class User(models.Model):
# #     username = models.CharField(max_length=25, Required=True)
#     username = models.CharField(max_length=100, null=True)
#     user_fname = models.CharField(max_length=50, null=False)
#     user_lname = models.CharField(max_length=50, null   =False)
#     user_email = models.EmailField(null=False)
#     user_password = models.CharField(max_length=50, null=False)
# #     liked_songs = models.ManyToManyField('Musicdata', blank=True)
#     objects = UserManager
