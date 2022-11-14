from recommender.models import Album, Artist

def findArtistDuplicates():

    print(f"Querying Database...")
    artists = Artist.objects.all()
    artistList = list(artists)
    
    print(f"Generating Result List...")
    artistResults = []
    
    print(f"Starting Artist Iterations...")
    for artist in artistList:
        currArtist = Artist.objects.filter(artist_name=artist.artist_name)
        currArtist = list(currArtist)
        print(f"\t- {artist.artist_name} - Length: {len(currArtist)}")
        if len(currArtist) > 1:
            artistResults.append([currArtist, len(currArtist)])
    print(f"Total Duplicate Artists: {len(artistResults)}")
    return artistResults
    
def findAlbumDuplicates():
    print(f"Querying Database...")
    albums = Album.objects.all()
    albumList = list(albums)

    print(f"Generating Result Playlists...")
    albumResults = []

    print(f"Starting Album Iterations...")
    for album in albumList:
        currAlbum = Album.objects.filter(album_name=album.album_name, album_artist=album.album_artist)
        currAlbum = list(currAlbum)
        print(f"\t- {album.album_name} - Length: {len(currAlbum)}")
        if len(currAlbum) > 1:
            albumResults.append([album.album_name, album.album_artist, len(currAlbum)])
    print(f"Total Duplicate Albums: {len(albumResults)}")
    return albumResults    

def fixAlbums(albumList):
    fixed = []
    broken = []
    for album in albumList:
        # Query for album by artist then compare amount
        currAlbum = Album.objects.filter(album_name=album[0], album_artist=album[1])
        currList = list(currAlbum)
        if len(currList) == album[2]:
            # Loop through currList and find album with most songs
            most = ["", 0]
            for curr in currList:
                if len(curr.album_tracks) > most[1]:
                    most = [curr.album_id, len(curr.album_tracks)]
            # Store album with most tracks
            top = currAlbum.get(curr.album_id)
            currList.remove(top)
            # Iterate through and add songs to top
            for curr2 in currList:
                for track in curr2.album_tracks:
                    top.album_tracks.add(track)
                    top.save()
                fixed.append(curr2)
                Album.objects.get(album_id=curr2.album_id).remove()
                Album.save()
        else:
        # The albums where total from albumList[2] != total albums with same name and artist
            broken.append(album)
    result = [fixed, broken]
    return result


    