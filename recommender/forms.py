from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from recommender.models import ProfileItems


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
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(
        widget=forms.TextInput(attrs={'size': '50'}))
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
    def __init__(self, *args, **kwargs):
        super(UpdateSettingsForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateProfileItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateProfileItemsForm, self).__init__(*args, **kwargs)

        self.fields['profile_items'].widget.attrs['class'] = 'form-control'
        self.fields['profile_items'].widget.attrs['placeholder'] = 'Profile Items'

    class Meta:
        model = ProfileItems
        fields = (
            'profile_pic',
            'bio'
        )

        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'})
        }


class UpdateProfilePictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateProfilePictureForm, self).__init__(*args, **kwargs)

        self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
        self.fields['profile_pic'].widget.attrs['placeholder'] = 'Profile Picture'

    class Meta:
        model = ProfileItems
        fields = (
            'profile_pic',
        )

        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UpdatePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2'
        )

        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class AddSongForm(forms.Form):
    song_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    song_artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
