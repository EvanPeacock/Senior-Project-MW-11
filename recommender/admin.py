from django.contrib import admin
from .models import Musicdata
from .models import DislikedMusic

# Register your models here.
admin.site.register(Musicdata)
admin.site.register(DislikedMusic)

