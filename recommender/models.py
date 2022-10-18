from django.db import models  
import random
from email.policy import default
from enum import unique
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

def unique_rand():
        index = random.randint(1,100000000)
        while True:
            if not Playlist.objects.filter(playlist_id=index).exists():
                return index
            else:
                index += 1

def unique_rand():
    index = 0
    while True:
        # code = password = User.objects.make_random_password(length=8)
        if not Playlist.objects.filter(playlist_id=index).exists():
            return index
        else:
            index += 1

class Musicdata(models.Model):
    track_id = models.TextField()
    track_name = models.TextField()
    track_artist = models.TextField()
    track_popularity  = models.FloatField()
    track_album_id  = models.TextField()
    track_album_name = models.TextField()
    track_album_release_date = models.IntegerField()
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
    # playlist_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    playlist_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    playlist_name = models.CharField(max_length=50, null=True, blank=False, default='New Playlist')
    playlist_owner = models.ManyToManyField(User, null=True, blank=True)
    playlist_songs = models.ManyToManyField('Musicdata', blank=True, null=True)
    
    def creator(self):
        author = list(self.playlist_owner.all())
        return str(author[0].username)
    
class RecentSearches(models.Model):
    artist = models.CharField(max_length=50)
    from_year = models.IntegerField(null=True, blank=True,)
    to_year = models.IntegerField(null=True, blank=True,)
    result1 = models.CharField(max_length=25, null=True, blank=True)
    result2 = models.CharField(max_length=25, null=True, blank=True)
    result3 = models.CharField(max_length=25, null=True, blank=True)
    
class song(models.Model):
    track_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    track_name = models.TextField()
    artist_id = models.TextField()
    track_album_id  = models.TextField()
    track_album_release_date = models.IntegerField() 
    playlist_id = models.ManyToManyField('playlist')
    duration_ms = models.IntegerField()

    def __str__(self): 
        return self.track_name

class artist(models.Model):
    artist_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    artist_name = models.TextField( null=True, blank=True)
    genre = models.TextField( null=True, blank=True)
    subgenre = models.TextField( null=True, blank=True)
    track_id = models.ManyToManyField(song, null=True, blank=True)

    def __str__(self): 
        return self.artist_name 

class album(models.Model):
    album_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    album_name = models.TextField( null=True, blank=True)
    track_id = models.ManyToManyField(song, null=True, blank=True)
    artist_id = models.ManyToManyField(artist, null=True, blank=True)
    genre = models.TextField()
    subgenre = models.TextField()

    def __str__(self): 
        return self.album_name

#class songtoplaylist(models.Model):
   # track_id = models.ForeignKey('song', on_delete=models.CASCADE)
    #playlist_id = models.ForeignKey('playlist',  on_delete=models.CASCADE)
