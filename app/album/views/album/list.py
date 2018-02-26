from django.shortcuts import render

from ...models import Album

__all__ = (
    'album_list',
)


def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'album/album_list.html', context)
