from django.contrib import admin
from .models import Musicdata

# Register your models here.
@admin.register(Musicdata)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['track_name', 'track_album_name', 'track_artist', 'duration_ms']

