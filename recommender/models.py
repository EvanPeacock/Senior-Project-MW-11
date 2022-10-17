<<<<<<< Updated upstream
=======
from email.policy import default
from enum import unique
>>>>>>> Stashed changes
from django.db import models  

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
    
<<<<<<< Updated upstream
# class User(models.Model):
# #     username = models.CharField(max_length=25, Required=True)
#     username = models.CharField(max_length=100, null=True)
#     user_fname = models.CharField(max_length=50, null=False)
#     user_lname = models.CharField(max_length=50, null   =False)
#     user_email = models.EmailField(null=False)
#     user_password = models.CharField(max_length=50, null=False)
# #     liked_songs = models.ManyToManyField('Musicdata', blank=True)
#     objects = UserManager
=======
    def __str__(self):
        return self.track_name
    
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
    from_year = models.IntegerField(blank=True, null=True)
    to_year = models.IntegerField(blank=True, null=True)
    result1 = models.CharField(max_length=25, null=True, blank=True)
    result2 = models.CharField(max_length=25, null=True, blank=True)
    result3 = models.CharField(max_length=25, null=True, blank=True)
>>>>>>> Stashed changes
