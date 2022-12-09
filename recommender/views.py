import random
from pickle import GET
from .models import *
from .forms import RegisterForm, SigninForm, UpdateSettingsForm, UpdatePasswordForm, SearchForm, PlaylistForm, ProfilePictureForm, BioForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect


def get_home(request):
    songs = Musicdata.objects.all()
    sResp = list(songs)
    random.shuffle(sResp)

    albums = Album.objects.all()
    alResp = list(albums)
    random.shuffle(alResp)

    artists = Artist.objects.all()
    arResp = list(artists)
    random.shuffle(arResp)

    popularPlaylists = Playlist.objects.all()
    pResp = list(popularPlaylists)
    random.shuffle(pResp)

    if request.user.is_authenticated:
        owner = User.objects.get(username=request.user.username)
        userPlaylists = Playlist.objects.filter(playlist_owner=owner)
        dislikes = Dislikes.objects.filter(user=owner)

        getDislikedSongs = dislikes.values_list('tracks', flat=True)
        dislikedSongs = []
        for track in getDislikedSongs:
            if track:
                dislikedSongs.append(Musicdata.objects.get(id=track))

        getDislikedArtists = dislikes.values_list('artists', flat=True)
        dislikedArtists = []
        for artist in getDislikedArtists:
            if artist:
                dislikedArtists.append(Artist.objects.get(artist_id=artist))

        getDislikedAlbums = dislikes.values_list('albums', flat=True)
        dislikedAlbums = []
        for album in getDislikedAlbums:
            if album:
                dislikedAlbums.append(Album.objects.get(album_id=album))

        getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
        dislikedPlaylists = []
        for p in getDislikedPlaylists:
            if p:
                dislikedPlaylists.append(
                    Playlist.objects.get(playlist_id=str(int(p)-1)))
    else:
        userPlaylists = []
        dislikedSongs = []
        dislikedAlbums = []
        dislikedArtists = []
        dislikedPlaylists = []

    args = {
        'songs': sResp[:3],
        'albums': alResp[:3],
        'artists': arResp[:3],
        'popularPlaylists': pResp[:3],
        'playlists': userPlaylists,
        'dislikedSongs': dislikedSongs,
        'dislikedAlbums': dislikedAlbums,
        'dislikedArtists': dislikedArtists,
        'dislikedPlaylists': dislikedPlaylists
    }

    return render(request, "recommender/home.html", args)


def get_explore(request):
    songs = Musicdata.objects.all()
    sResp = list(songs)
    random.shuffle(sResp)
    albums = Album.objects.all()
    alResp = list(albums)
    random.shuffle(alResp)
    playlists = Playlist.objects.all()
    pResp = list(playlists)
    random.shuffle(pResp)
    artists = Artist.objects.all()
    arResp = list(artists)
    random.shuffle(arResp)
    userResp = User.objects.all()
    uResp = list(userResp)
    random.shuffle(uResp)

    if request.user.is_authenticated:

        owner = User.objects.get(username=request.user.username)
        userPlaylists = Playlist.objects.filter(playlist_owner=owner)
        dislikes = Dislikes.objects.filter(user=owner)

        getDislikedSongs = dislikes.values_list('tracks', flat=True)
        dislikedSongs = []
        for track in getDislikedSongs:
            if track:
                dislikedSongs.append(Musicdata.objects.get(id=track))

        getDislikedArtists = dislikes.values_list('artists', flat=True)
        dislikedArtists = []
        for artist in getDislikedArtists:
            if artist:
                dislikedArtists.append(Artist.objects.get(artist_id=artist))

        getDislikedAlbums = dislikes.values_list('albums', flat=True)
        dislikedAlbums = []
        for album in getDislikedAlbums:
            if album:
                dislikedAlbums.append(Album.objects.get(album_id=album))

        getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
        dislikedPlaylists = []
        for p in getDislikedPlaylists:
            if p:
                dislikedPlaylists.append(
                    Playlist.objects.get(playlist_id=str(int(p)-1)))

        friends = FriendsList.objects.filter(user=request.user).values_list('friends')
        friendsList = list(friends)
        friendsDislikeSongList = []
        friendsDislikeAlbumList = []
        friendsDislikePlaylistList = []
        if friendsList:
            for friend in friendsList:
                friendsDislikes = Dislikes.objects.filter(user=friend)
                getFriendsDislikedSongs = friendsDislikes.values_list('tracks',flat=True)
                getFriendsDislikedAlbums = friendsDislikes.values_list('albums',flat=True)
                getFriendsDislikedPlaylists = friendsDislikes.values_list('playlists',flat=True)
                for track in getFriendsDislikedSongs:
                    if track:
                        friendsDislikeSongList.append(Musicdata.objects.get(id=track))
                for album in getFriendsDislikedAlbums:
                    if album:
                        friendsDislikeAlbumList.append(Album.objects.get(album_id=album))
                for playlist in getFriendsDislikedPlaylists:
                    if playlist:
                        friendsDislikePlaylistList.append(Playlist.objects.get(playlist_id=str(int(playlist) - 1)))
            random.shuffle(friendsDislikeSongList)
            random.shuffle(friendsDislikeAlbumList)
            random.shuffle(friendsDislikePlaylistList)
    else:
        userPlaylists = []
        dislikedSongs = []
        dislikedAlbums = []
        dislikedArtists = []
        dislikedPlaylists = []
        friendsDislikeSongList = []
        friendsDislikeAlbumList = []
        friendsDislikePlaylistList = []

    args = {
        'songs': sResp[:3],
        'albums': alResp[:3],
        'recPlaylists': pResp[:3],
        'artists': arResp[:3],
        'users': uResp[:10],
        'playlists': userPlaylists,
        'dislikedSongs': dislikedSongs,
        'dislikedAlbums': dislikedAlbums,
        'dislikedArtists': dislikedArtists,
        'dislikedPlaylists': dislikedPlaylists,
        'friendsDislikeSongList': friendsDislikeSongList[:3],
        'friendsDislikeAlbumList': friendsDislikeAlbumList[:3],
        'friendsDislikePlaylistList': friendsDislikePlaylistList[:3],
    }
    return render(request, "recommender/explore.html", args)


def find_albums(artist, from_year=None, to_year=None):
    query = Musicdata.objects.filter(track_artist__contains=artist)
    if from_year is not None:
        query = query.filter(track_album_release_date__gte=from_year)
    if to_year is not None:
        query = query.filter(track_album_release_date__lte=to_year)
    # return list(query.order_by('-track_popularity').values('track_id'))
    return list(query.order_by('-track_popularity'))


def find_album_by_name(album):
    query = Album.objects.filter(album_name__contains=album)
    resp = list(query)
    # Randomize to get different results each time
    random.shuffle(resp)
    # Return the id of up to 3 albums
    return {
        'albums': resp[:3]
    }


def find_track_by_name(track):
    query = Musicdata.objects.filter(
        track_name__contains=track)
    resp = list(query)
    # Randomize to get different results each time
    random.shuffle(resp)
    # Return the id of up to 3 albums
    return {
        'tracks': [*set([item for item in resp[:3]])]
    }


def get_artist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
            playlists = Playlist.objects.filter(playlist_owner=owner)
        else:
            playlists = []
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            from_year = None if form.cleaned_data['from_year'] == None else int(
                form.cleaned_data['from_year'])
            to_year = None if form.cleaned_data['to_year'] == None else int(
                form.cleaned_data['to_year'])
            albums = find_albums(
                form.cleaned_data['artist'],
                from_year,
                to_year
            )

            # Random 3 of top 10 popular albums
            answers = albums[:10]
            random.shuffle(answers)
            if len(answers) > 0:
                answers = list(answers)[:3]
                rs = RecentSearches.objects.create()
                rs.artist = form.cleaned_data['artist']
                rs.from_year = from_year
                rs.to_year = to_year
                rs.result1 = answers[0].track_id
                rs.result2 = answers[1].track_id
                rs.result3 = answers[2].track_id
                rs.save()
            else:
                answers = []
            args = {
                'form': form,
                'answers': answers,
                'playlists': playlists
            }
            return render(request, 'recommender/artist.html', args)
        else:
            raise Http404('Something went wrong')
    else:
        form = SearchForm()
        return render(request, 'recommender/artist.html', {'form': form})


def get_album(request):
    if request.method == 'GET':
        album = request.GET.get('album', None)
        if album is None:
            return render(request, "recommender/album.html", {})
        else:
            albums = {}
            if album != "":
                albums = find_album_by_name(album)
            return render(request, "recommender/results.html", albums)


def get_track(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
            playlists = Playlist.objects.filter(playlist_owner=owner)
        else:
            playlists = []
        track = request.GET.get('track', None)
        if track is None:
            return render(request, "recommender/track.html", {'playlists': playlists})
        else:
            tracks = {}
            if track != "":
                tracks = find_track_by_name(track)
            args = {
                'tracks': tracks['tracks'],
                'playlists': playlists
            }
            return render(request, "recommender/results2.html", args)


def get_signin(request):
    err = ''
    if request.method == 'POST':
        form = SigninForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/recommender/myprofile')
    else:
        form = SigninForm
        args = {'form': form}
        return render(request, 'recommender/signin.html', args)
    form = SigninForm
    err = 'Invalid Username or Password'
    args = {'form': form, 'err': err}
    return render(request, 'recommender/signin.html', args)


def get_registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/recommender/myprofile')
            else:
                raise Http404('Error with user')
        else:
            return redirect('/recommender/registration/')
    else:
        form = RegisterForm
        args = {'form': form}
        return render(request, 'recommender/register.html', args)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        raise Http404('Error logging out')


def get_profile(request, user_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            dislikes = Dislikes.objects.filter(user=user)
            getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
            dislikedPlaylists = []
            for p in getDislikedPlaylists:
                if p:
                    dislikedPlaylists.append(
                        Playlist.objects.get(playlist_id=str(int(p)-1)))
        else:
            dislikedPlaylists = []
        if user_name is not None:
            owner = User.objects.get(username=user_name)
            playlists = Playlist.objects.filter(playlist_owner=owner)
            getFriends = FriendsList.objects.filter(
            friends__username=user_name).values_list('user', flat=True)
            followers = []
            for friend in getFriends:
                followers.append(User.objects.get(id=friend))
            getFollowing = FriendsList.objects.filter(
                user=owner).values_list('friends', flat=True)
            following = []
            print('getFollowing')
            if getFollowing.exists() and getFollowing[0] is not None:
                print(list(getFollowing))
                for friend in getFollowing:
                    following.append(User.objects.get(id=friend))
            getBio = Bio.objects.filter(
                user=owner).values_list('bio', flat=True)
            bio = getBio[0] if len(getBio) > 0 else None
            args = {
                'profile_user': owner,
                'playlists': playlists,
                'followers' : followers[:3],
                'following' : following[:3],
                'bio': bio,
                'dislikedPlaylists': dislikedPlaylists,
            }
            return render(request, 'recommender/profile.html', args)
        else:
            return render(request, 'recommender/signin.html', {})
    else:
        raise render('Unable to access profile')


def get_myprofile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            owner = request.user
            dislikes = Dislikes.objects.filter(user=owner)
            getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
            dislikedPlaylists = []
            for p in getDislikedPlaylists:
                if p:
                    dislikedPlaylists.append(
                        Playlist.objects.get(playlist_id=str(int(p)-1)))
            playlists = list(Playlist.objects.filter(playlist_owner=owner))
            random.shuffle(playlists)
            getFriends = FriendsList.objects.filter(
            friends__username=owner).values_list('user', flat=True)
            followers = []
            for friend in getFriends:
                followers.append(User.objects.get(id=friend))
            getFollowing = FriendsList.objects.filter(
                user=owner).values_list('friends', flat=True)
            print(getFollowing)
            following = []
            if getFollowing.exists() and getFollowing[0] is not None:
                for friend in getFollowing:
                    following.append(User.objects.get(id=friend))
            getBio = Bio.objects.filter(
                user=owner).values_list('bio', flat=True)
            bio = getBio[0] if len(getBio) > 0 else None

            args = {
                'playlists': playlists[:3],
                'bio': bio,
                'followers' : followers[:3],
                'following' : following[:3],
                'dislikedPlaylists': dislikedPlaylists,
            }
            return render(request, 'recommender/myprofile.html', args)
        else:
            return render(request, 'recommender/signin.html', {})
    else:
        raise render('Unable to access profile')


def get_settings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'recommender/edit_settings.html', {})
    else:
        return redirect('recommender/home/')


def update_settings(request):
    if request.method == 'POST':
        form = UpdateSettingsForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/recommender/myprofile/')
    else:
        form = UpdateSettingsForm(instance=request.user)
        args = {'form': form}
        return render(request, 'recommender/edit_settings.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST, user=request.user)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/recommender/myprofile/')
        else:
            return redirect('/recommender/password/')
    else:
        form = UpdatePasswordForm(data=request.POST, user=request.user)
        args = {'form': form}
        return render(request, 'recommender/change_password.html', args)


def playlist_view(request, playlist_num):
    playlist = Playlist.objects.get(playlist_id=playlist_num)

    if request.user.is_authenticated:
        owner = User.objects.get(username=request.user.username)
        dislikes = Dislikes.objects.filter(user=owner)

        getDislikedSongs = dislikes.values_list('tracks', flat=True)
        dislikedSongs = []
        for track in getDislikedSongs:
            if track:
                dislikedSongs.append(Musicdata.objects.get(id=track))

        getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
        dislikedPlaylists = []
        for p in getDislikedPlaylists:
            if p:
                dislikedPlaylists.append(
                    Playlist.objects.get(playlist_id=str(int(p)-1)))

        if owner == playlist.playlist_owner:
            getUserPlaylists = Playlist.objects.filter(playlist_owner=owner)
            playlists = list(getUserPlaylists)
            playlists.remove(playlist)
        else:
            playlists = Playlist.objects.filter(playlist_owner=owner)
    else:
        playlists = []
        dislikedSongs = []
        dislikedPlaylists = []

    args = {
        'playlist': playlist,
        'playlists': playlists,
        'dislikedSongs': dislikedSongs,
        'dislikedPlaylists': dislikedPlaylists
    }

    return render(request, 'recommender/playlist.html', args)


def get_playlists(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            dislikes = Dislikes.objects.filter(user=user)
            getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
            dislikedPlaylists = []
            for p in getDislikedPlaylists:
                if p:
                    dislikedPlaylists.append(
                        Playlist.objects.get(playlist_id=str(int(p)-1)))
        else:
            dislikedPlaylists = []
        playlists = Playlist.objects.all()
        args = {
            'playlists': playlists,
            'dislikedPlaylists': dislikedPlaylists
        }
        return render(request, 'recommender/playlists.html', args)
    else:
        return Http404('Error getting playlists')


def get_user_playlists(request, user_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            dislikes = Dislikes.objects.filter(user=user)
            getDislikedPlaylists = dislikes.values_list('playlists', flat=True)
            dislikedPlaylists = []
            for p in getDislikedPlaylists:
                if p:
                    dislikedPlaylists.append(
                        Playlist.objects.get(playlist_id=str(int(p)-1)))
        else:
            dislikedPlaylists = []
        owner = User.objects.get(username=user_name)
        playlists = Playlist.objects.filter(playlist_owner=owner)
        args = {
            'playlists': playlists,
            'owner': owner,
            'dislikedPlaylists': dislikedPlaylists
        }

        return render(request, 'recommender/playlists.html', args)
    else:
        return Http404('Error finding user playlists')


def create_playlist(request, user_name):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            p_name = None if form.cleaned_data['playlist_name'] == None else form.cleaned_data['playlist_name']
            # p_id = None if form.cleaned_data['playlist_id'] == None else form.cleaned_data['playlist_id']
            p_owner = User.objects.filter(username=user_name)
            p_songs = []
            # p_songs = None if form.cleaned_data['playlist_songs'] == None else form.cleaned_data['playlist_songs']

            playlist = Playlist.objects.create()
            playlist.playlist_name = p_name
            playlist.playlist_owner.set(p_owner)
            playlist.playlist_songs.set(p_songs)

            playlist.save()

            return redirect('/recommender/playlist/' + str(playlist.playlist_id))
        else:
            return Http404('Error: Invalid form')
    else:
        form = PlaylistForm()
        return render(request, "recommender/playlists.html", {'form': form})


def get_following(request, user_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            getFriends = FriendsList.objects.filter(
                user=user).values_list('friends', flat=True)
            print(getFriends)
            following = []
            if getFriends.exists() and getFriends[0] is not None:
                for friend in getFriends:
                    following.append(User.objects.get(id=friend))
            args = {
                'following': following,
                'user_name': user_name
            }
            return render(request, 'recommender/following.html', args)
        else:
            return render(request, 'recommender/signin.html', {})
    else:
        return Http404('Error getting friends')


def get_followers(request, user_name):
    if request.method == 'GET':
        getFriends = FriendsList.objects.filter(
            friends__username=user_name).values_list('user', flat=True)
        followers = []
        for friend in getFriends:
            followers.append(User.objects.get(id=friend))

        args = {
            'followers': followers,
            'user_name': user_name
        }
        return render(request, 'recommender/followers.html', args)
    else:
        return Http404('Error getting followers')


def following_list_append(request, friend_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            friend = User.objects.get(username=friend_name)
            if FriendsList.objects.filter(user=user).exists():
                print('User already has a friends list')
                friends_list = FriendsList.objects.get(user=user)
                friends_list.friends.add(friend)
                print('Friend added to friends list')
                print(friend)
                print(friends_list.friends.all())
                friends_list.save()
            else:
                print("Creating new friends list")
                friends_list = FriendsList.objects.create(user=user)
                friends_list.friends.add(friend)
                friends_list.save()
            return redirect('/recommender/following/' + request.user.username)
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def following_list_remove(request, friend_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            friend = User.objects.get(username=friend_name)
            if FriendsList.objects.filter(user=user).exists():
                print('User already has a friends list')
                friends_list = FriendsList.objects.get(user=user)
                friends_list.friends.remove(friend)
                print('Friend removed from friends list')
                print(friend)
                print(friends_list.friends.all())
                friends_list.save()
            else:
                print("Creating new friends list")
                friends_list = FriendsList.objects.create(user=user)
                friends_list.friends.remove(friend)
                friends_list.save()
            return redirect('/recommender/following/' + request.user.username)
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def get_history(request):
    if request.method == "GET":
        try:
            searches = RecentSearches.objects.all().order_by('-search_datetime')
            return render(request, "recommender/history.html", {'searches': searches})
        except:
            raise Http404('Error with searches')
    else:
        raise Http404('Error')


def get_dislikes(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        playlists = Playlist.objects.filter(playlist_owner=user)

        dislikes = Dislikes.objects.filter(user=user)

        getTracks = dislikes.values_list('tracks', flat=True)
        tracks = []
        for track in getTracks:
            if track:
                tracks.append(Musicdata.objects.get(id=track))

        getArtists = dislikes.values_list('artists', flat=True)
        artists = []
        for artist in getArtists:
            if artist:
                artists.append(Artist.objects.get(artist_id=artist))

        getAlbums = dislikes.values_list('albums', flat=True)
        albums = []
        for album in getAlbums:
            if album:
                albums.append(Album.objects.get(album_id=album))

        getPlaylists = dislikes.values_list('playlists', flat=True)
        dislikedPlaylists = []
        for playlist in getPlaylists:
            if playlist:
                dislikedPlaylists.append(Playlist.objects.get(
                    playlist_id=str(int(playlist)-1)))
    else:
        playlists = []

    args = {
        'dislikes': dislikes,
        'dislikedSongs': tracks,
        'dislikedArtists': artists,
        'dislikedAlbums': albums,
        'dislikedPlaylists': dislikedPlaylists,
        'playlists': playlists
    }
    return render(request, 'recommender/dislikes.html', args)


def dislike_song(request, user_name, track_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            tracks = Musicdata.objects.filter(track_id=track_id)
            track = tracks[0]
            dislikes.tracks.add(track)
            print(dislikes.tracks.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def dislike_artist(request, user_name, artist_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            artist = Artist.objects.get(artist_id=artist_id)
            dislikes.artists.add(artist)
            print(dislikes.artists.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def dislike_album(request, user_name, album_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            album = Album.objects.get(album_id=album_id)
            dislikes.albums.add(album)
            print(dislikes.albums.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def dislike_playlist(request, user_name, playlist_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            playlist = Playlist.objects.get(playlist_id=playlist_id)
            print(playlist.playlist_name)
            print(playlist.playlist_id)
            dislikes.playlists.add(playlist)
            print(dislikes.playlists.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def undislike_song(request, user_name, track_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            tracks = Musicdata.objects.filter(track_id=track_id)
            track = tracks[0]
            dislikes.tracks.remove(track)
            print(dislikes.tracks.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def undislike_artist(request, user_name, artist_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            artist = Artist.objects.get(artist_id=artist_id)
            dislikes.artists.remove(artist)
            print(dislikes.artists.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def undislike_album(request, user_name, album_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            album = Album.objects.get(album_id=album_id)
            dislikes.albums.remove(album)
            print(dislikes.albums.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def undislike_playlist(request, user_name, playlist_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(username=user_name)
            if Dislikes.objects.filter(user=user).exists():
                dislikes = Dislikes.objects.get(user=user)
            else:
                dislikes = Dislikes.objects.create(user=user)
            playlist = Playlist.objects.get(playlist_id=playlist_id)
            dislikes.playlists.remove(playlist)
            print(dislikes.playlists.all())
            dislikes.save()
            return redirect('/recommender/dislikes/')
        else:
            return redirect('/recommender/signin/')
    else:
        raise Http404('Error')


def add_song_update(request, playlist_num):
    if request.method == 'GET':
        track = request.GET.get('song', None)
        if track is None:
            return render(request, "recommender/add_song_update.html", {'playlist_num': playlist_num})
        else:
            tracks = {}
            if track != "":
                query = Musicdata.objects.filter(
                    track_name__contains=track).values('track_id')
                tracks = list(query)
                songs = list([*set([item['track_id'] for item in tracks[:3]])])
                args = {'playlist_num': playlist_num, 'songs': songs}
            return render(request, "recommender/results3.html", args)


def remove_song(request, playlist_num, song_id):
    if request.method == 'GET':
        playlist = Playlist.objects.filter(playlist_id=playlist_num).first()
        song = Musicdata.objects.filter(track_id=song_id).first()
        playlist.playlist_songs.remove(song)
        args = {
            'playlist': playlist,
            'song_id': song_id
        }
        return render(request, 'recommender/playlist.html', args)
    else:
        return Http404('Error removing song from playlist')


def playlist_append(request, playlist_num, song_id):
    if request.method == 'GET':
        song = Musicdata.objects.filter(track_id=song_id)
        song = list(song.order_by('-track_popularity'))
        playlist = Playlist.objects.get(playlist_id=playlist_num)
        playlist.playlist_songs.add(song[0])
        playlist.save()
        args = {'playlist_num': playlist_num, 'song_id': song_id}
        return redirect(request.META.get('HTTP_REFERER'), args)
    else:
        raise Http404('Error')


def view_album(request, album_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
            playlists = Playlist.objects.filter(playlist_owner=owner)
        else:
            playlists = []
        album = Album.objects.get(album_id=album_id)
        args = {
            'album': album,
            'playlists': playlists
        }
        return render(request, 'recommender/album_view.html', args)
    else:
        raise Http404('Error')


def view_artist(request, artist_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
            playlists = Playlist.objects.filter(playlist_owner=owner)
        else:
            playlists = []
        artist = Artist.objects.get(artist_name=artist_name)
        artist_albums = Album.objects.filter(album_artist=artist)
        artist_albums = artist_albums.order_by('album_name')
        args = {
            'artist': artist,
            'playlists': playlists,
            'artist_albums': artist_albums
        }
        return render(request, 'recommender/artist_view.html', args)
    else:
        raise Http404('Error')

def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            if ProfilePicture.objects.filter(user=user).exists():
                print("exists")
                profile_picture = ProfilePicture.objects.get(user=user)
                profile_picture.delete()
            else:
                profile_picture = ProfilePicture(user=user)

            profile_picture = ProfilePicture(
                user=user, profile_picture=request.FILES['profile_picture'])
            profile_picture.save()
            return redirect('recommender:get_myprofile')
    else:
        form = ProfilePictureForm()
    return render(request, 'recommender/my_profile.html', {'form': form})


def update_bio(request):
    if request.method == 'POST':
        form = BioForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            if Bio.objects.filter(user=user).exists():
                bio = Bio.objects.get(user=user)
                bio.delete()
            else:
                bio = Bio(user=user)

            bio = Bio(user=user, bio=request.POST['bio'])
            bio.save()
            return redirect('recommender:get_myprofile')
    else:
        print('not post')
        form = UpdateSettingsForm(instance=request.user)
        args = {'form': form}
        return render(request, 'recommender/edit_bio.html', args)


def post_sign_in(request):
    return redirect('recommender:get_myprofile')
