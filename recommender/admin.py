from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


# Register your models here.
@admin.register(Musicdata)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['track_name', 'track_album_name', 'track_artist', 'duration_ms']


admin.site.register(RecentSearches)

@admin.register(Playlist)
class playlisttAdmin(admin.ModelAdmin):
     list_display = ['playlist_id', 'playlist_name']

@admin.register(Album)
class albumAdmin(admin.ModelAdmin):
     list_display = ['album_name', 'album_artist', 'album_id']

@admin.register(Artist)
class artistAdmin(admin.ModelAdmin):
     list_display = ['artist_name', 'artist_id']

@admin.register(FriendsList)
class friendsAdmin(admin.ModelAdmin):
     list_display = ['user']

@admin.register(ProfilePicture)
class profilePictureAdmin(admin.ModelAdmin):
     list_display = ['user']

@admin.register(Bio)
class bioAdmin(admin.ModelAdmin):
     list_display = ['user']

@admin.register(Dislikes)
class dislikesAdmin(admin.ModelAdmin):
     list_display = ['user']
