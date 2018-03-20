from django.urls import path

from ..apis.artist import ArtistListView, ArtistDetailView

app_name = 'artist'
urlpatterns = [
    path('', ArtistListView.as_view(), name='artist-list'),
    path('<int:pk>/', ArtistDetailView.as_view(), name='artist-detail'),
]
