from django.shortcuts import render

from utils import *

__all__ = [
    'artist_search_from_melon',
]


def artist_search_from_melon(request):
    """
    Template: artist/artist_search_from_melon.html
        form (input한개, button한개)
    1. form에 주어진 'keyword'로 멜론 사이트의 아티스트 검색 결과를 크롤링
    2. 크롤링 된 검색 결과를 적절히 파싱해서 검색 결과 목록을 생성
        -> list내에 dict들을 만드는 형태
        artist_info_list = [
            {'name':'아이유', 'url_image_cover': 'http:...'},
            {'name':'아이유', 'url_image_cover': 'http:...'},
            {'name':'아이유', 'url_image_cover': 'http:...'},
        ]
    3. 해당 결과 목록을 템플릿에 출력
        context = {'artist_info_list': artist_infi_list}로 전달 후 템플릿에서 사용
    :param request:
    :return:
    """
    context = dict()

    try:
        keyword = request.GET['keyword'].strip()
    except KeyError as e:
        print('Key Error', e)
        keyword = None

    if keyword:
        params = {
            'q': keyword,
        }
        soup = get_response(url=f'https://www.melon.com/search/artist/index.htm', params=params)

        artist_info_list = list()
        for artist_li in soup.select('#pageList > div > ul > li'):
            artist_name = artist_li.select_one('div > div > dl > dt > a').get_text()
            artist_url_image_cover = artist_li.select_one('div > a > img').get('src')
            artist_id = artist_li.select_one('div > div > dl > dd.wrap_btn > button')['data-artist-no']
            artist_info_list.append({
                'artist_id': artist_id,
                'name': artist_name,
                'url_image_cover': artist_url_image_cover,
            })
        context['artist_info_list'] = artist_info_list

    return render(request, 'artist/artist_search_from_melon.html', context)
