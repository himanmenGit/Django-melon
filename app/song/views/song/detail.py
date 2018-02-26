from django.shortcuts import render, get_object_or_404

from ...models import Song

__all__ = (
    'song_detail',
)


def song_detail(request, song_pk):
    context = {
        'song': get_object_or_404(Song, pk=song_pk)
    }
    return render(request, 'song/song_detail.html', context)
