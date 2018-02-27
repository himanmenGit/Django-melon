from django.contrib import admin

from .models import Artist, ArtistLike, YoutubeLike

admin.site.register(Artist)
admin.site.register(ArtistLike)
admin.site.register(YoutubeLike)