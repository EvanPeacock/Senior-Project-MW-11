from django.db import models
import random
from email.policy import default
from enum import unique
from django.db import models  
import random, uuid
from django.contrib.auth.models import User

def unique_rand():
    index = random.randint(1, 100000000)
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
            
def uniqueIDArtist():
    randList = []
    for _ in range(random.randint(10,100)):
        randList.append(random.randint(100000000000, 999999999999))
    return random.choice(randList)



class Musicdata(models.Model):
    track_id = models.TextField()
    track_name = models.TextField()
    track_artist = models.TextField()
    track_popularity = models.FloatField()
    track_album_id = models.TextField()
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
    
    def __str__(self):
        return self.track_name
        
class Playlist(models.Model):
    playlist_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    playlist_name = models.CharField(max_length=50, null=True, blank=False, default='New Playlist')
    playlist_owner = models.ManyToManyField(User, null=True, blank=True)
    playlist_songs = models.ManyToManyField('Musicdata', blank=True, null=True)
    
    def creator(self):
        author = list(self.playlist_owner.all())
        return str(author[0].username)


class RecentSearches(models.Model):
    artist = models.CharField(max_length=50)
    from_year = models.IntegerField(null=True, blank=True)
    to_year = models.IntegerField(null=True, blank=True)
    result1 = models.CharField(max_length=25, null=True, blank=True)
    result2 = models.CharField(max_length=25, null=True, blank=True)
    result3 = models.CharField(max_length=25, null=True, blank=True)
    
# For some reason, when Artist or Album object is created, the  
# track lists are created with a full list. 
#   - I got around this by reseting them on creation in script.py
#   - Maybe can be fixed by altering __init__?

class Artist(models.Model):
    artist_id = models.TextField(primary_key=True, default=uniqueIDArtist, editable=False)
    artist_name = models.CharField(max_length=25, blank=True, null=True)
    # artist_albums = models.ManyToManyField(Album, blank=True, null=True)
    artist_tracks = models.ManyToManyField('Musicdata', blank=True, null=True)
    artist_genre = models.CharField(max_length=25, blank=True, null=True)
    artist_subgenre = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        return str(self.artist_name)

class Album(models.Model):
    album_id = models.TextField(null=True, blank=True)
    album_name = models.CharField(max_length=50, blank=True, null=True)
    album_tracks = models.ManyToManyField('Musicdata', blank=True, null=True)
    album_artist = models.TextField(blank=True, null=True)
    album_release_date = models.IntegerField(null=True, blank=True)
    album_genre = models.CharField(max_length=25, blank=True, null=True)
    album_subgenre = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        return self.album_name

class song(models.Model):
    track_id = models.CharField(max_length=8, unique=True, default=unique_rand)
    track_name = models.TextField()
    artist_id = models.TextField()
    track_album_id = models.TextField()
    track_album_release_date = models.IntegerField()
    playlist_id = models.ManyToManyField('playlist')
    duration_ms = models.IntegerField()

    def __str__(self):
        return self.track_name


class DislikedMusic(models.Model):
    user = models.ManyToManyField(User, blank=True)
    music = models.ManyToManyField(Musicdata, blank=True)


class ProfileItems(models.Model):
    user = models.ManyToManyField(User, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)


# class songtoplaylist(models.Model):
   # track_id = models.ForeignKey('song', on_delete=models.CASCADE)
    #playlist_id = models.ForeignKey('playlist',  on_delete=models.CASCADE)
