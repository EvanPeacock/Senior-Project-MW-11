# Script being written to populate Album and Artist tables with data 
# by iterating through the Musicdata objects. It then will check for 
# if there already is an Artist or Album with those specifications.

# Import models from models.py and time for timer
from recommender.models import Musicdata, Album, Artist
import time

# Start the timer
timerStart = time.time()

# --  Start Artist Portion -- 
print(f"\n\n *** Starting Artist Portion *** \n")

# Query musicdata objects and store in list
songQuery = Musicdata.objects.all()
songList = list(songQuery)

# Setup counters to keep track of object number
totalArtistCounter = 0 # Artist Counters
totalArtistCreations = 0
totalArtistAdditions = 0

totalAlbumCounter = 0 # Album Counters
totalAlbumCreations = 0
totalAlbumAdditions = 0

# Iterate through each object
for song in songList:
    
    # Print details
    print(f"\t - {totalArtistCounter}: {song.track_name} by {song.track_artist} - ")
    
    # Query information needed for check
    artist_name = song.track_artist
    
    # Check for existence
    if Artist.objects.filter(artist_name=artist_name):
        
        # Check to see if song already added
        if not Artist.objects.filter(artist_tracks__track_id=song.track_id):
            
            # Add song to artist's tracks
            currArtist = Artist.objects.get(artist_name=artist_name)
            currArtist.artist_tracks.add(song)
            
            # Save the object
            currArtist.save()
            
            # Increment totalAdditions
            totalArtistAdditions = totalArtistAdditions + 1
    else:
        # Create new object, set name and add song
        newArtist = Artist.objects.create()
        newArtist.artist_name = artist_name
        newArtist.artist_tracks.clear()
        newArtist.artist_tracks.add(song)
        
        # Save the object
        newArtist.save()
        
        # Increment totalCreations and totalAdditions
        totalArtistCreations = totalArtistCreations + 1
        totalArtistAdditions = totalArtistAdditions + 1
        
    # Increment totalCounter to keep track of object number
    totalArtistCounter = totalArtistCounter + 1     

# --  Start Artist Portion -- 
print(f"\n\n *** Starting Artist Portion *** \n")

# Query artist objects and store in list
artistQuery = Artist.objects.all()
artistList = list(artistQuery)

# Iterate through each object
for song in songList:
    
    # Print details
    print(f"\t - {totalAlbumCounter}: {song.track_name} by {song.track_artist} - ")
    
    # Query information needed for check
    album_id = song.track_album_id
    album_name = song.track_album_name
    album_release_date = song.track_album_release_date
    album_artist = song.track_artist
    
    # Check for existence
    if Album.objects.filter(album_name=album_name, album_artist=album_artist):
        
        # Check to see if song already added
        if not Album.objects.filter(album_tracks__track_id=song.track_id):
            
            # Add song to album's tracks
            currAlbum = Album.objects.get(album_name=album_name, album_artist=album_artist)
            currAlbum.album_tracks.add(song)
            
            # Save the object
            currAlbum.save()
            
            # Increment totalAdditions
            totalAlbumAdditions = totalAlbumAdditions + 1
    else:
        # Create new object, set name and add song
        newAlbum = Album.objects.create()
        newAlbum.album_id_original = album_id
        newAlbum.album_name = album_name
        newAlbum.album_release_date = album_release_date
        newAlbum.album_artist = album_artist
        newAlbum.album_tracks.clear()
        newAlbum.album_tracks.add(song)
        
        # Save the object
        newAlbum.save()
        
        # Increment totalCreations and totalAdditions
        totalAlbumCreations = totalAlbumCreations + 1
        totalAlbumAdditions = totalAlbumAdditions + 1
        
    # Increment totalCounter to keep track of object number
    totalAlbumCounter = totalAlbumCounter + 1     
    
# Stop timer
timerStop = time.time()
timer = timerStop - timerStart

# Calculate time
hours = int(timer/3600)
minutes = int((timer/60) - (hours*60))
seconds = int(timer - (minutes*60) - (hours*3600))

# Print ending details
albumQuery = Album.objects.all()
albumList = list(albumQuery)
print(f"\n\n****************************************\n\t -- End Metrics -- \n")
print(f" - Time duration: {hours}:{minutes}:{seconds}")
print(f" - Total Artists: {len(artistList)}")
print(f"\t - Total Artist Iterations: {totalArtistCounter} - \n\t - Total Artist Additions: {totalArtistAdditions} - \n\t - Total Artist Creations: {totalArtistCreations} - ")
print(f" - Total Albums: {len(albumList)}")
print(f"\t - Total Album Iterations: {totalAlbumCounter} - \n\t - Total Album Additions: {totalAlbumAdditions} - \n\t - Total Album Creations: {totalAlbumCreations} - ")