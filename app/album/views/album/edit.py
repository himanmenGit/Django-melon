from django.shortcuts import redirect, render, get_object_or_404

from ...form import AlbumForm
from ...models import Album

__all__ = (
    'album_edit',
)


def album_edit(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album:album-list')

    form = AlbumForm(instance=album)
    context = {'album_form': form}
    return render(request, 'album/album_edit.html', context)
