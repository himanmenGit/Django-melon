from django.shortcuts import render

from utils import *

__all__ = [
    'song_search_from_melon',
]


def song_search_from_melon(request):
    context = dict()

    try:
        keyword = request.GET['keyword'].strip()
    except KeyError as e:
        print('Key Error', e)
        keyword = None

    if keyword:
        params = {
            'q': keyword,
            'section': 'song',
        }

        soup = get_response(url=f'https://www.melon.com/search/song/index.htm', params=params)

        song_info_list = list()
        tr_list = soup.select('form#frm_defaultList > div > table > tbody > tr')
        for tr in tr_list:
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title_a = tr.select_one('td:nth-of-type(3) a.fc_gray')
            title_s = tr.select_one('td:nth-of-type(3) > div > div > span')
            if title_a:
                title = title_a.get_text(strip=True)
            else:
                title = title_s.get_text(strip=True)
            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)
            song_info_list.append({
                'song_id': song_id,
                'title': title,
                'artist': artist,
                'album': album,
            })
        context['song_info_list'] = song_info_list

    return render(request, 'song/song_search_from_melon.html', context)
