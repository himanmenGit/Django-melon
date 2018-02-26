from django.shortcuts import redirect

from ...models import Album

__all__ = (
    'album_like_toggle',
)


def album_like_toggle(request, album_pk):
    """
    request.user와
    album_pk를 사용해서

    AlbumLike객체를 토글하는 뷰

    완료 후에는
    :param request:
    :param album_pk:
    :return:
    """

    album = Album.objects.get(pk=album_pk)
    if request.method == 'POST':
        album.toggle_like_user(user=request.user)
        next_path = request.POST.get('next-path', 'album:album-list')
        return redirect(next_path)
