from django.shortcuts import render

from crawler import *

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
    else:
        context['artist_info_list'] = artist_search_from_melon_crawler(keyword)
    finally:
        return render(request, 'artist/artist_search_from_melon.html', context)
