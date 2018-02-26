from django.shortcuts import render

from crawler import *

__all__ = [
    'album_search_from_melon',
]


def album_search_from_melon(request):
    context = dict()

    try:
        keyword = request.GET['keyword'].strip()
    except KeyError as e:
        print('Key Error', e)
    else:
        context['album_info_list'] = album_search_from_melon_crawler(keyword)
    finally:
        return render(request, 'album/album_search_from_melon.html', context)
