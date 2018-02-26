from django.contrib import admin

from .models import Album, AlbumLike

admin.site.register(Album)
admin.site.register(AlbumLike)