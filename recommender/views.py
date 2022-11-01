
from enum import unique
from pickle import GET
import re
from recommender.forms import SearchForm
from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from .forms import PlaylistForm, RegisterForm, SearchForm, SigninForm, UpdateSettingsForm
import random
from django.http import Http404
from .models import Musicdata
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import PasswordChangeForm


def get_home(request):
    songs = Musicdata.objects.all().values('track_id')
    sResp = list(songs)
    random.shuffle(sResp)
    albums = Musicdata.objects.all().values('track_id')
    aResp = list(albums)
    random.shuffle(aResp)
    playlists = Musicdata.objects.all().values('track_id')
    pResp = list(playlists)
    random.shuffle(pResp)
    return render(request, "recommender/home.html", {
        'songs': sResp[:3],
        'albums': aResp[:3],
        'playlists': pResp[:3]
    })


def get_explore(request):
    songs = Musicdata.objects.all().values('track_id')
    sResp = list(songs)
    random.shuffle(sResp)
    albums = Musicdata.objects.all().values('track_id')
    aResp = list(albums)
    random.shuffle(aResp)
    playlists = Musicdata.objects.all().values('track_id')
    pResp = list(playlists)
    random.shuffle(pResp)
    userResp = User.objects.all()
    uResp = list(userResp)
    random.shuffle(uResp)
    return render(request, "recommender/explore.html", {
        'songs': sResp[:3],
        'albums': aResp[:3],
        'playlists': pResp[:3],
        'users': uResp[:10]
    })


def find_albums(artist, from_year=None, to_year=None):
    query = Musicdata.objects.filter(track_artist__contains=artist)
    if from_year is not None:
        query = query.filter(track_album_release_date__gte=from_year)
    if to_year is not None:
        query = query.filter(track_album_release_date__lte=to_year)
    return list(query.order_by('-track_popularity').values('track_id'))


def find_album_by_name(album):
    query = Musicdata.objects.filter(
        track_album_name__contains=album).values('track_id')
    resp = list(query)
    # Randomize to get different results each time
    random.shuffle(resp)
    # Return the id of up to 3 albums
    return {
        'albums': [item['track_id'] for item in resp[:3]]
    }


def find_track_by_name(track):
    query = Musicdata.objects.filter(
        track_name__contains=track).values('track_id')
    resp = list(query)
    # Randomize to get different results each time
    random.shuffle(resp)
    # Return the id of up to 3 albums
    return {
        'tracks': [*set([item['track_id'] for item in resp[:3]])]
    }


def get_artist(request):
    if request.method == 'POST':
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
            answer = albums[:10]
            random.shuffle(answer)
            answer = list(answer)[:3]
            rs = RecentSearches.objects.create()
            rs.artist = form.cleaned_data['artist']
            rs.from_year = from_year
            rs.to_year = to_year
            rs.result1 = answer[0]
            rs.result2 = answer[1]
            rs.result3 = answer[2]
            rs.save()
            return render(request, 'recommender/artist.html', {'form': form, 'albums': answer})
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
        track = request.GET.get('track', None)
        if track is None:
            return render(request, "recommender/track.html", {})
        else:
            tracks = {}
            if track != "":
                tracks = find_track_by_name(track)
            return render(request, "recommender/results2.html", tracks)


def get_signin(request):
    if request.method=='POST':
        form = SigninForm(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/recommender/myprofile')
    else:
        form = SigninForm
        args = {'form': form}
        return render(request, 'recommender/signin.html', args)
    return render(request, "recommender/signin.html")

def get_registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/recommender/myprofile/')
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
            return render(request, 'recommender/profile.html', {
                'songs': sResp[:3],
                'albums': aResp[:3],
                'profile_user': user_name,
                'user_object': owner,
                'playlists': playlists
                })
        else:
            return render(request, 'recommender/signin.html', {})
    else:
        raise render('Unable to access profile')


def get_myprofile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            songs = Musicdata.objects.all().values('track_id')
            sResp = list(songs)
            random.shuffle(sResp)
            albums = Musicdata.objects.all().values('track_id')
            aResp = list(albums)
            random.shuffle(aResp)
            owner = request.user
            playlists = list(Playlist.objects.filter(playlist_owner=owner))
            random.shuffle(playlists)
            return render(request, 'recommender/myprofile.html', {
                'songs': sResp[:3],
                'albums': aResp[:3],
                'playlists': playlists
                })
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
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/recommender/myprofile/')
        else:
            return redirect('/recommender/password/')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        args = {'form':form}
        return render(request,'recommender/change_password.html',args)

def playlist_view(request, playlist_num):
    # try:
    playlist = Playlist.objects.get(playlist_id=playlist_num)
    potential_songs = Musicdata.objects.all()
    return render(request, 'recommender/playlist.html', {'playlist':playlist, 'potential_songs':potential_songs})
    # except:
    #     raise Http404('Could not display playlist')
    
def get_playlists(request):
    if request.method == 'GET':
        playlists = Playlist.objects.all()
        return render(request, 'recommender/playlists.html', {'playlists':playlists})
    else:
        return Http404('Error getting playlists')
    
def get_user_playlists(request, user_name):
    if request.method == 'GET':
        owner = User.objects.get(username=user_name)
        playlists = Playlist.objects.filter(playlist_owner=owner)
        return render(request, 'recommender/playlists.html', {'playlists':playlists, 'owner':owner})
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
            
            return render(request, "recommender/playlists.html", {'form':form, 'user':p_owner})
        else:
            return Http404('Error: Invalid form')
    else:
        form = PlaylistForm()
        return render(request, "recommender/playlists.html", {'form':form})
    
def get_history(request):
    if request.method == "GET":
        try:
            searches = RecentSearches.objects.all()
            return render(request, "recommender/history.html", {'searches':searches})
        except:
            raise Http404('Error with searches')
    else:
        raise Http404('Error')

def dislike(request, user_name, song):
    if request.method == 'GET':
        try:
            curUser = User.objects.filter(username=user_name).first()
            music = Musicdata.objects.filter(track_id__contains = song).first()
            dislikedMusic = DislikedMusic.objects.get(user = curUser)
            dislikedMusic.save()
            music.save()
            dislikedMusic.music.add(music)
            return render(request, "recommender/track.html", {})
        except:
            curUser = User.objects.filter(username=user_name).first()
            dislikedMusic = DislikedMusic()
            dislikedMusic.save()
            curUser.save()
            dislikedMusic.user.add(curUser)
            music = Musicdata.objects.filter(track_id__contains = song).first()
            music.save()
            dislikedMusic.music.add(music)   
            return render(request, "recommender/track.html", {})
    else:
        return Http404('Error adding song to dislikes')

def get_dislikes(request):
    if request.method == 'GET':
        curUser = request.user
        dislikes = DislikedMusic.objects.all()
        disliked = dislikes.filter(user = curUser)
        songs = []
        for song in disliked:
            songs.append(song.music.values('track_id'))
        return render(request, 'recommender/dislikes.html', {'dislikes':songs})
    else:
        return Http404('Error getting dislikes')

def undislike(request, user_name, song):
    if request.method == 'GET':
        curUser = User.objects.filter(username=user_name).first()
        dislike = DislikedMusic.objects.get(user = curUser)
        track = Musicdata.objects.filter(track_id = song).first()
        dislike.music.remove(track)
        disliked = DislikedMusic.objects.filter(user = curUser)
        songs = []
        for song in disliked:
            songs.append(song.music.values('track_id'))
        return render(request, 'recommender/dislikes.html', {'dislikes':songs})
    else:
        return Http404('Error removing song from dislikes')
            