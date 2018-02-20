import re
from bs4 import NavigableString
from django.http import HttpResponse
from django.shortcuts import redirect

from ...models import Artist

__all__ = [
    'artist_add_from_melon',
]


def get_artist_dt_dd(soup, css_selector, is_span_tag=False):
    dt_dd_list = list()
    artist_dl = soup.select_one(css_selector)
    if artist_dl:
        for dt, dd in zip(artist_dl.find_all('dt'), artist_dl.find_all('dd')):
            dt_dd_list.append(dt.get_text(strip=True))
            if is_span_tag:
                dt_dd_span = dd.select_one('span')
                if dt_dd_span:
                    dt_dd_list.append(dt_dd_span.get_text(strip=True))
                else:
                    dt_dd_list.append(dd.get_text(strip=True))
            else:
                dt_dd_list.append(dd.get_text(strip=True))

        dt_dd_iter = iter(dt_dd_list)
        return dict(zip(dt_dd_iter, dt_dd_iter))
    else:
        return {}


def get_detail(artist_id):
    import requests
    from bs4 import BeautifulSoup

    request_url = 'https://www.melon.com/artist/detail.htm'
    request_params = {
        'artistId': artist_id
    }
    response = requests.get(request_url, request_params)
    soup = BeautifulSoup(response.text, 'lxml')

    if not soup:
        return

    artist_info_dict = dict()
    # ==================== 간단 정보 ===================== #

    # 아티스트 간단 프로필 div
    artist_simple_div = soup.select_one('#conts > div.wrap_dtl_atist > div > div.wrap_atist_info')

    # 아티스트 이름
    artist_name = artist_simple_div.select_one('p')
    if artist_name:
        artist_info_dict['name'] = artist_name.get_text()

    # 아티스트 신상 정보
    artist_detail_normal_info = get_artist_dt_dd(soup, '#conts > div.section_atistinfo04 > dl')
    artist_info_dict['info'] = artist_detail_normal_info

    # 아티스트 소개
    if soup.select_one('#conts > div.section_atistinfo02'):
        artist_detail_introduce_div = soup.find('div', id='d_artist_intro')
        introduce_list = list()
        for item in artist_detail_introduce_div.contents:
            if item.name == 'br':
                introduce_list.append('\n')
            elif type(item) is NavigableString:
                introduce_list.append(item.strip())

        artist_detail_introduce = ''.join(introduce_list)
        artist_info_dict['intro'] = artist_detail_introduce
    return artist_info_dict


def artist_add_from_melon(request):
    """
    POST 요청을 받음
    request.POST['artist_id']

    artist_id를 사용해서
    멜론사이트에서 Artist에 들어갈 상세정보들을 가져옴

    artist_id
    name
    real_name
    nationality
    birth_date
    constellation
    blood_type
    intro

    를 채운 Artist를 생성, DB에 저장
    :param request:
    :return:
    """
    if request.method == 'POST':
        artist_info_dict = dict()
        try:
            artist_id = request.POST['artist_id']
            artist_info_dict = get_detail(artist_id)
            artist_name = request.POST['artist_name']
        except Exception as e:
            print(e)

        name = artist_name
        real_name = artist_info_dict['info']['본명']
        nationality = artist_info_dict['info']['국적']
        birth_date = artist_info_dict['info']['생일']
        constellation = artist_info_dict['info']['별자리']
        blood_type = artist_info_dict['info']['혈액형']
        intro = artist_info_dict['intro']

        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
        else:
            blood_type = Artist.BLOOD_TYPE_OTHER

        from datetime import datetime
        artist, created = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date, '%Y.%m.%d'),
                'constellation': constellation,
                'blood_type': blood_type,
                'intro': intro,
            }
        )
        print(artist)
        print(created)
    return redirect('artist:artist-list')
