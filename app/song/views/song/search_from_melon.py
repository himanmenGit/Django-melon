from django.shortcuts import render

from crawler import *

__all__ = [
    'song_search_from_melon',
]


def song_search_from_melon(request):
    context = dict()

    try:
        keyword = request.GET['keyword'].strip()
    except KeyError as e:
        print('Key Error', e)
    else:
        context['song_info_list'] = song_search_from_melon_crawler(keyword)
    finally:
        return render(request, 'song/song_search_from_melon.html', context)
