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
    path('', views.get_home, name='get_home'),
    path('explore/', views.get_explore, name='get_explore'),
    path('dislikes/', views.get_dislikes, name= 'get_dislikes'),
    path('dislike/<slug:user_name>/<slug:song>/',views.dislike, name='dislike'),
    path('undislike/<slug:user_name>/<slug:song>/', views.undislike, name='undislike')
]
 