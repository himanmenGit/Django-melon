from rest_framework import generics

from utils.pagination import SmallSetPagination
from ...serializers import ArtistSerializer
from ...models import Artist

__all__ = (
    'ArtistListView',
    'ArtistDetailView',
)


class ArtistListView(generics.ListCreateAPIView):
    # getnerics의 요소를 사용해서
    # ArtistListCreateView,
    # ArtistRetrieveUpdateDestroyView
    #   2개를 구현
    #   URL과 연결
    #   Postman에 API 테스트 구현
    #   다 실행해보기
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    pagination_class = SmallSetPagination

    def get(self, request, *args, **kwargs):
        print('request.user:', request.user)
        # return self.list(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
