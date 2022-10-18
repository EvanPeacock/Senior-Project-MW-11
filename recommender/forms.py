from django import forms
from django.forms import ModelForm

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

class UpdateSettingsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'size':'50'}))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={'size':'50'}))
    user_fname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    user_lname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    

