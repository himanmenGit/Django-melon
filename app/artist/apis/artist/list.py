from rest_framework import generics, permissions

from utils.pagination import SmallPagination
from ...serializers import ArtistSerializer
from ...models import Artist

__all__ = (
    'ArtistListCreateView',
    'ArtistRetrieveUpdateDestroyVIew',
)


class ArtistListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    pagination_class = SmallPagination


class ArtistRetrieveUpdateDestroyVIew(generics.RetrieveUpdateDestroyAPIView):

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
