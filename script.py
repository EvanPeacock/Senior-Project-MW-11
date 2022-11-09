# Script being written to populate Album and Artist tables with data 
# by iterating through the Musicdata objects. It then will check for 
# if there already is an Artist or Album with those specifications.
# If so, it will .

# Import models from models.py and time for timer
from recommender.models import Musicdata, Album, Artist
import time

# Instantiate Timer
timeStart = time.time()

# --  Start Artist Portion -- 
print(f"\n\n *** Starting Artist Portion *** ")

# Query musicdata objects and store in list
songQuery = Musicdata.objects.all()
songList = list(songQuery)

# Setup counters to keep track of object number
totalArtistCounter = 0 # Artist Counters
totalArtistreations = 0
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
        if not Artist.objects.get(track_id=song.track_id):
            
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
        newArtist.artist_tracks.add(song)
        
        # Save the object
        newArtist.save()
        
        # Increment totalCreations and totalAdditions
        totalArtistCreations = totalArtistCreations + 1
        totalArtistAdditions = totalArtistAdditions + 1
        
    # Increment totalCounter to keep track of object number
    totalArtistCounter = totalArtistCounter + 1     

# --  Start Artist Portion -- 
print(f"\n\n *** Starting Artist Portion *** ")

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
    
    # Check for existence
    if Album.objects.filter(album_id=album_id):
        
        # Check to see if song already added
        if not Album.objects.filter(track_id=song.track_id):
            
            # Add song to artist's tracks
            Album.objects.get(album_id=album_id).album_tracks.add(song)
            
            # Increment totalAdditions
            totalAlbumAdditions = totalAlbumAdditions + 1
    else:
        # Create new object, set name and add song
        newAlbum = Album.objects.create()
        newAlbum.album_id = album_id
        newAlbum.album_name = album_name
        newAlbum.album_release_date = album_release_date
        newAlbum.album_tracks.add(song)
        
        # Save the object
        newAlbum.save()
        
        # Increment totalCreations and totalAdditions
        totalAlbumCreations = totalAlbumCreations + 1
        totalAlbumAdditions = totalAlbumAdditions + 1
        
    # Increment totalCounter to keep track of object number
    totalAlbumCounter = totalAlbumCounter + 1     
    
# Calculate timer
timeStop = time.time()
timer = timeStop - timeStart

# Timer calculations
hours = int(timer/3600)
minutes = int((timer/60) - (hours*60))
seconds = int(timer - (hours*3600) - (minutes*60))
    
# Print ending details
albumQuery = Album.objects.all()
albumList = list(albumQuery)
print(f"\n\n****************************************\n\t -- End Metrics -- \n")
print(f" - Total Time: {hours}h:{minutes}m:{seconds}s")
print(f" - Total Artists: {artistList.length}")
print(f"\t - Total Artist Iterations: {totalArtistCounter} - \n\t - Total Artist Additions: {totalArtistAdditions} - \n\t - Total Artist Creations: {totalArtistCreations} - ")
print(f" - Total Albums: {albumList.length}")
print(f"\t - Total Album Iterations: {totalAlbumCounter} - \n\t - Total Album Additions: {totalAlbumAdditions} - \n\t - Total Album Creations: {totalAlbumCreations} - ")