from dataclasses import field
from secrets import choice
from django import forms
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from recommender.models import Musicdata, Playlist
# from .models import User

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    user_fname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    user_lname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={'size':'50'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'50'}))

class SigninForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'50'}))
    
class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    # playlist_songs = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=[(song.track_id, song.__str__()) for song in Musicdata.objects.all()])

# class PlaylistForm(forms.ModelForm):
#     class Meta:
#         model = Playlist
#         fields = ['playlist_name', 'playlist_songs']
#         widgets = {
#             'playlist_name': forms.TextInput(attrs={'placeholder': 'Playlist Name'}),
#             'playlist_songs': forms.SelectMultiple(choices=Musicdata.objects.all()),
#         } 

class UpdateSettingsForm(UserChangeForm):
    class Meta:
    
        model = User
        
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control',}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'})
        }