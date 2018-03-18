from rest_framework.response import Response
from rest_framework.views import APIView

from ...serializers import ArtistSerializer
from ...models import Artist

__all__ = (
    'ArtistListView',
)


class ArtistListView(APIView):
    def get(self, requset):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
