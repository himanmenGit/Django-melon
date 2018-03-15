from django.urls import path

from .. import apis

ap_name = 'artist'
urlpatterns = [
    path('', apis.artist_list, name='artist-list'),
]
