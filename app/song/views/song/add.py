from django.shortcuts import redirect, render

from ...form import SongForm

__all__ = [
    'song_add',
]


def song_add(request):
    context = {

    }
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song:song-list')
    else:
        form = SongForm()

    context['song_form'] = form
    return render(request, 'song/song_add.html', context)
