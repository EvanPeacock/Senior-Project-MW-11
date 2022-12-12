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
    path('myprofile/profile_pic/', views.update_profile_picture, name='update_profile_picture'),
    path('myprofile/edit_bio/', views.update_bio, name='edit_bio'),
    path('myprofile/update_bio/', views.update_bio, name='update_bio'),
    path('myprofile/settings/',views.get_settings,name="get_settings"),
    path('myprofile/update_settings/',views.update_settings,name="update_settings"),
    path('myprofile/password/', views.change_password, name="change_password"),
    
    path('history/', views.get_history, name='get_history'),

    path('artist/', views.get_artist, name='get_artist'),
    path('album/', views.get_album, name='get_album'),
    path('track/', views.get_track, name='get_track'),
    path('user/', views.get_user, name='get_user'),
    
    path('playlist/', views.get_playlists, name='get_playlists'),
    path('playlist/<int:playlist_num>/', views.playlist_view, name='playlist_view'),
    path('playlist/<str:user_name>/', views.get_user_playlists, name='get_user_playlists'),
    path('playlist/create/<str:user_name>/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_num>/add_song_update', views.add_song_update, name='add_song_update'),
    path('playlist/<int:playlist_num>/add_song_update/<str:song_id>', views.playlist_append, name="playlist_append"),
    path('playlist/<int:playlist_num>/remove_song_update/<str:song_id>', views.remove_song, name="remove_song"),

    path('following/<str:user_name>', views.get_following, name='get_following'),
    path('follow/<str:friend_name>', views.following_list_append, name='add_friend'),
    path('unfollow/<str:friend_name>', views.following_list_remove, name='remove_friend'),
    path('followers/<str:user_name>', views.get_followers, name='get_followers'),

    path('dislikes/', views.get_dislikes, name= 'get_dislikes'),
    path('dislikes/<str:user_name>', views.get_dislikes, name= 'get_dislikes'),
    path('dislike/song/<str:user_name>/<str:track_id>', views.dislike_song, name='dislike_song'),
    path('undislike/song/<str:user_name>/<str:track_id>/', views.undislike_song, name='undislike_song'),
    path('dislike/album/<str:user_name>/<str:album_id>', views.dislike_album, name='dislike_album'),
    path('undislike/album/<str:user_name>/<str:album_id>/', views.undislike_album, name='undislike_album'),
    path('dislike/artist/<str:user_name>/<str:artist_id>', views.dislike_artist, name='dislike_artist'),
    path('undislike/artist/<str:user_name>/<str:artist_id>/', views.undislike_artist, name='undislike_artist'),
    path('dislike/playlist/<str:user_name>/<str:playlist_id>', views.dislike_playlist, name='dislike_playlist'),
    path('undislike/playlist/<str:user_name>/<str:playlist_id>/', views.undislike_playlist, name='undislike_playlist'),
    
    path('album/<str:album_id>/', views.view_album, name="view_album"),
    path('artist/<str:artist_name>/', views.view_artist, name="view_artist"),
]
 