from django.db import models  
import random
from email.policy import default
from enum import unique

def unique_rand():
        index = random.randint(1,100000000)
        while True:
            if not playlist.objects.filter(playlist_id=index).exists():
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
    
    def __str__(self): 
        return self.track_name
    
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

class playlist(models.Model):
    track_id = models.ManyToManyField(song,  null=True, blank=True)
    playlist_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    playlist_name = models.TextField( null=True, blank=True)
    user_id = models.TextField( null=True, blank=True)
    
    def __str__(self): 
        return self.playlist_name

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
