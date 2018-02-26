from django.shortcuts import render, get_object_or_404

from ...models import Album

__all__ = (
    'album_detail',
)


def album_detail(request, album_pk):
    context = {
        'album': get_object_or_404(Album, pk=album_pk)
    }
    return render(request, 'album/album_detail.html', context)
