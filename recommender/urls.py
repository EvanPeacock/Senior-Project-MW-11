from unicodedata import name
from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('', views.get_home, name='get_home'),
    path('home/', views.get_home, name='get_home'),
    path('explore/', views.get_explore, name='get_explore'),

    path('signin/', views.get_signin, name='get_signin'),
    path('registration/', views.get_registration, name='get_registration'),
    path('logout/',views.logout_view,name="logout_view"),
    path('logout_view/', views.logout_view, name='logout_view'),

    path('profile/<str:user_name>', views.get_profile, name='get_profile'),
    path('myprofile/', views.get_myprofile,name='get_myprofile'),
    path('myprofile/settings/',views.get_settings,name="get_settings"),
    path('update-settings/',views.update_settings,name="update_settings"),
    path('password/', views.change_password, name="change_password"),
    
    path('history/', views.get_history, name='get_history'),

    path('artist/', views.get_artist, name='get_artist'),
    path('album/', views.get_album, name='get_album'),
    path('track/', views.get_track, name='get_track'),
    
    path('playlist/', views.get_playlists, name='get_playlists'),
    path('playlist/<int:playlist_num>/', views.playlist_view, name='playlist_view'),
    path('playlist/<str:user_name>/', views.get_user_playlists, name='get_user_playlists'),
    path('playlist/create/<str:user_name>/', views.create_playlist, name='create_playlist'),

    path('dislikes/', views.get_dislikes, name= 'get_dislikes'),
    path('dislike/<slug:user_name>/<slug:song>/',views.dislike, name='dislike'),
    path('undislike/<slug:user_name>/<slug:song>/', views.undislike, name='undislike')
]
 