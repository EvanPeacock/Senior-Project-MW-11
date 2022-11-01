from dataclasses import field
import email
from secrets import choice
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'

        )
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control',}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'})
        }

class SigninForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'})
        }
        
    
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
            'last_name'
        )

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control',}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'})
        }