from django.contrib import admin
<<<<<<< Updated upstream
from .models import Musicdata
=======
from .models import Musicdata, Playlist, RecentSearches
from django.contrib.auth.models import User
>>>>>>> Stashed changes

# Register your models here.
admin.site.register(Musicdata)

<<<<<<< Updated upstream
=======
admin.site.register(Playlist)

admin.site.register(RecentSearches)
>>>>>>> Stashed changes
