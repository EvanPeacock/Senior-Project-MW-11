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
    songs = Musicdata.objects.all().values('track_id')
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
    else:
        userPlaylists = []

    args = {
        'songs': sResp[:3],
        'albums': alResp[:3],
        'artists': arResp[:3],
        'popularPlaylists': pResp[:3],
        'playlists': userPlaylists
    }

    return render(request, "recommender/home.html", args)


def get_explore(request):
    songs = Musicdata.objects.all().values('track_id')
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
        playlists = Playlist.objects.filter(playlist_owner=owner)
    else:
        playlists = []

    args = {
        'songs': sResp[:3],
        'albums': alResp[:3],
        'playlists': pResp[:3],
        'artists': arResp[:3],
        'users': uResp[:10],
        'userPlaylists': playlists
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
            answers = list(answers)[:3]
            rs = RecentSearches.objects.create()
            rs.artist = form.cleaned_data['artist']
            rs.from_year = from_year
            rs.to_year = to_year
            rs.result1 = answers[0].track_id
            rs.result2 = answers[1].track_id
            rs.result3 = answers[2].track_id
            rs.save()
            answer = [answers[0].track_id, answers[1].track_id, answers[2].track_id]
            args = {
                'form': form,
                'albums': answer,
                'answers':answers,
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
        if user_name is not None:
            owner = User.objects.get(username=user_name)
            playlists = Playlist.objects.filter(playlist_owner=owner)
            songs = Musicdata.objects.all().values('track_id')
            sResp = list(songs)
            random.shuffle(sResp)
            albums = Musicdata.objects.all().values('track_id')
            aResp = list(albums)
            random.shuffle(aResp)
            getBio = Bio.objects.filter(user=owner).values_list('bio', flat=True)
            bio = getBio[0] if len(getBio) > 0 else None
            args = {
                'profile_user': owner,
                'playlists': playlists,
                'songs': sResp[:3],
                'albums': aResp[:3],
                'bio': bio
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
            playlists = list(Playlist.objects.filter(playlist_owner=owner))
            random.shuffle(playlists)

            getBio = Bio.objects.filter(user=owner).values_list('bio', flat=True)
            bio = getBio[0] if len(getBio) > 0 else None

            args = {
                'playlists': playlists[:3],
                'bio': bio,
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
        if owner == playlist.playlist_owner:
            getPlaylists = Playlist.objects.filter(playlist_owner=owner)
            playlists = list(getPlaylists)
            playlists.remove(playlist)
            disliked_songs = get_disliked_music(request)
        else:
            playlists = Playlist.objects.filter(playlist_owner=owner)
    else:
        playlists = []
        disliked_songs = []

    args = {
        'playlist': playlist,
        'playlists': playlists,
        'disliked_songs': disliked_songs
    }

    return render(request, 'recommender/playlist.html', args)


def get_playlists(request):
    if request.method == 'GET':
        playlists = Playlist.objects.all()
        return render(request, 'recommender/playlists.html', {'playlists': playlists})
    else:
        return Http404('Error getting playlists')


def get_user_playlists(request, user_name):
    if request.method == 'GET':
        owner = User.objects.get(username=user_name)
        playlists = Playlist.objects.filter(playlist_owner=owner)
        return render(request, 'recommender/playlists.html', {'playlists': playlists, 'owner': owner})
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
            getFriends = FriendsList.objects.filter(user=user).values_list('friends', flat=True)
            print (getFriends)
            following = []
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
        getFriends = FriendsList.objects.filter(friends__username=user_name).values_list('user', flat=True)
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


def dislike(request, user_name, song):
    if request.method == 'GET':
        try:
            curUser = User.objects.filter(username=user_name).first()
            music = Musicdata.objects.filter(track_id__contains=song).first()
            dislikedMusic = DislikedMusic.objects.get(user=curUser)
            dislikedMusic.save()
            music.save()
            dislikedMusic.music.add(music)
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            curUser = User.objects.filter(username=user_name).first()
            dislikedMusic = DislikedMusic()
            dislikedMusic.save()
            curUser.save()
            dislikedMusic.user.add(curUser)
            music = Musicdata.objects.filter(track_id__contains=song).first()
            music.save()
            dislikedMusic.music.add(music)
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return Http404('Error adding song to dislikes')


def get_disliked_music(request):
    disliked = DislikedMusic.objects.all().filter(user=request.user)
    songs = []
    for song in disliked:
        songs.append(song.music.values('track_id'))

    args = {
        'dislikes': songs
    }
    return args


def get_dislikes(request):
    if request.method == 'GET':
        disliked = DislikedMusic.objects.all().filter(user=request.user)
        songs = []
        for song in disliked:
            songs.append(song.music.values('track_id'))

        args = {
            'dislikes': songs
        }
        return render(request, 'recommender/dislikes.html', args)
    else:
        return Http404('Error getting dislikes')


def undislike(request, user_name, song):
    if request.method == 'GET':
        curUser = User.objects.filter(username=user_name).first()
        dislike = DislikedMusic.objects.get(user=curUser)
        track = Musicdata.objects.filter(track_id=song).first()
        dislike.music.remove(track)
        disliked = DislikedMusic.objects.filter(user=curUser)
        songs = []
        for song in disliked:
            songs.append(song.music.values('track_id'))
        args = {
            'dislikes': songs
        }
        return render(request, 'recommender/dislikes.html', args)
    else:
        return Http404('Error removing song from dislikes')


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
            
            profile_picture = ProfilePicture(user=user, profile_picture=request.FILES['profile_picture'])
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