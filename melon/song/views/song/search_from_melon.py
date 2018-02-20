from django.http import HttpResponse

__all__ = [
    'song_search_from_melon',
]


def song_search_from_melon(requset):
    return HttpResponse('song_search_from_melon')
