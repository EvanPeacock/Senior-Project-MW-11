import random
from django.db import models  
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone


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

class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name

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
    playlist_owner = models.ManyToManyField(User, blank=True)
    playlist_songs = models.ManyToManyField('Musicdata', blank=True)
    
    def creator(self):
        author = list(self.playlist_owner.all())
        return str(author[0].username)

class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    
    def __str__(self):
        return self.user.username

class ProfilePicture(models.Model):
    def pfp_rename(instance, filename):
        new_filename = "%s.jpg" % (instance.user.username)
        return new_filename

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=pfp_rename, storage=OverwriteStorage(), blank=True, null=True)

    def __str__(self):
        return self.user.username

class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username


class RecentSearches(models.Model):
    artist = models.CharField(max_length=50)
    from_year = models.IntegerField(null=True, blank=True)
    to_year = models.IntegerField(null=True, blank=True)
    result1 = models.CharField(max_length=25, null=True, blank=True)
    result2 = models.CharField(max_length=25, null=True, blank=True)
    result3 = models.CharField(max_length=25, null=True, blank=True)
    search_datetime = models.DateTimeField(blank=True, default=timezone.now())
    
# For some reason, when Artist or Album object is created, the  
# track lists are created with a full list. 
#   - I got around this by reseting them on creation in script.py
#   - Maybe can be fixed by altering __init__?

class Artist(models.Model):
    artist_id = models.TextField(primary_key=True, default=uniqueIDArtist, editable=False)
    artist_name = models.CharField(max_length=25, blank=True, null=True)
    artist_albums = models.ManyToManyField('Album', blank=True)
    artist_tracks = models.ManyToManyField('Musicdata', blank=True)
    artist_genre = models.CharField(max_length=25, blank=True, null=True)
    artist_subgenre = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        return str(self.artist_name)

class Album(models.Model):
    album_id = models.TextField(primary_key=True, default=uniqueIDArtist, editable=False)
    album_id_original = models.TextField(null=True, blank=True)
    album_name = models.CharField(max_length=50, blank=True, null=True)
    album_tracks = models.ManyToManyField('Musicdata', blank=True)
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

# class songtoplaylist(models.Model):
   # track_id = models.ForeignKey('song', on_delete=models.CASCADE)
    #playlist_id = models.ForeignKey('playlist',  on_delete=models.CASCADE)
