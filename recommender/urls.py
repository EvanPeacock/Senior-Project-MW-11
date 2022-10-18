from unicodedata import name
from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('artist/', views.get_artist, name='get_artist'),
    path('album/', views.get_album, name='get_album'),
    path('track/', views.get_track, name='get_track'),
    path('registration/', views.get_registration, name='get_registration'),
    path('signin/', views.get_signin, name='get_signin'),
    path('home/', views.get_home, name='get_home'),
    path('myprofile/', views.get_profile,name='get_profile'),
    path('logout/',views.logout_view,name="logout_view"),
    path('update-settings/',views.update_settings,name="update_settings"),
    path('myprofile/settings/',views.get_settings,name="get_settings")
]
 