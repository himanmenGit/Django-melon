from django.urls import path

from ..apis.artist import ArtistListCreateView, ArtistRetrieveUpdateDestroyVIew


app_name = 'artist'
urlpatterns = [
    path('', ArtistListCreateView.as_view(), name='artist-list'),
    path('<int:pk>', ArtistRetrieveUpdateDestroyVIew.as_view(), name='artist-detail'),
]
