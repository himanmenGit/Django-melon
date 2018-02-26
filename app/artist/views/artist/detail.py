from django.shortcuts import render, get_object_or_404

from ...models import Artist

__all__ = (
    'artist_detail',
)


def artist_detail(request, artist_pk):
    context = {
        'artist': get_object_or_404(Artist, pk=artist_pk)
    }
    return render(request, 'artist/artist_detail.html', context)
