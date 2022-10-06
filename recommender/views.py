
from recommender.forms import SearchForm
from django.shortcuts import render
from django.http import Http404
from .models import Musicdata
from .forms import RegisterForm, SearchForm, SigninForm
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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

def find_albums(artist, from_year = None, to_year = None):
    query = Musicdata.objects.filter(track_artist__contains = artist)
    if from_year is not None:
        query = query.filter(track_album_release_date__gte = from_year)
    if to_year is not None:
        query = query.filter(track_album_release_date__lte = to_year)
    return list(query.order_by('-track_popularity').values('track_id'))
    

def find_album_by_name(album):
    query = Musicdata.objects.filter(track_album_name__contains = album).values('track_id')
    resp = list(query)
    # Randomize to get different results each time
    random.shuffle(resp) 
    # Return the id of up to 3 albums
    return { 
        'albums': [item['track_id'] for item in resp[:3]]
    }

def find_track_by_name(track):
    query = Musicdata.objects.filter(track_name__contains = track).values('track_id')
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
            from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
            to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
            albums = find_albums(
                    form.cleaned_data['artist'],
                    from_year,
                    to_year
                )
            
            # Random 3 of top 10 popular albums
            answer = albums[:10]
            random.shuffle(answer)
            answer = list(answer)[:3] 
            return render(request, 'recommender/artist.html', {'form': form, 'albums': answer })
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
    err = ''
    if request.method == 'POST':
        try:
            form = SigninForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    return render(request, 'recommender/home.html', {'form':form, 'err':err})
                else:
                    err = 'Unable to authenticate account'
                    return render(request, 'recommender/signin.html', {'form':form, 'err':err})
        except:
            return render(request, 'recommender/signin.html', {'form':SigninForm(), 'err':'Authentification failed'})
    else:
        form = SigninForm()
        return render(request, "recommender/signin.html", {'form':form, 'err':'Problem occured'})
    
def get_registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        err = ''
        if form.is_valid():
            username = None if form.cleaned_data['username'] == None else str(form.cleaned_data['username'])
            fname = None if form.cleaned_data['user_fname'] == None else str(form.cleaned_data['user_fname'])
            lname = None if form.cleaned_data['user_lname'] == None else str(form.cleaned_data['user_lname'])
            email = None if form.cleaned_data['user_email'] == None else str(form.cleaned_data['user_email'])
            password = None if form.cleaned_data['user_password'] == None else form.cleaned_data['user_password']
            user = User.objects.create_user(username, email)
            user.first_name = fname
            user.last_name = lname
            user.set_password(password)
            user.save()
            return render(request, "recommender/register.html", {'form':form, 'user':user, 'err':err})
        else:
            err = 'All fields must be filled correctly.'
            return render(request, 'recommender/register.html', {
                'form':form,
                'err':err,
            })
    else:
        form = RegisterForm()
        return render(request, 'recommender/register.html', {'form':form})
