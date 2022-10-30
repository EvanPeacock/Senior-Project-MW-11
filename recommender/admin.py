from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


# Register your models here.
@admin.register(Musicdata)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['track_name', 'track_album_name', 'track_artist', 'duration_ms']


admin.site.register(RecentSearches)


@admin.register(song)
class songAdmin(admin.ModelAdmin):
     list_display = ['track_name', 'artist_id', 'duration_ms']

@admin.register(Playlist)
class playlisttAdmin(admin.ModelAdmin):
     list_display = ['playlist_name']

@admin.register(album)
class albumAdmin(admin.ModelAdmin):
     list_display = ['album_name']

@admin.register(artist)
class artistAdmin(admin.ModelAdmin):
     list_display = ['artist_name']

admin.register(DislikedMusic)
