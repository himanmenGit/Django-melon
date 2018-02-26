from bs4 import NavigableString, Tag

from .utils import *

__all__ = [
    'artist_search_from_melon_crawler',
    'get_artist_detail_crawler'
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


def get_artist_detail_crawler(artist_id):
    params = {
        'artistId': artist_id,
    }
    soup = get_response(url=f'https://www.melon.com/artist/detail.htm', params=params)

    if not soup:
        return

    artist_info_dict = dict()

    artist_simple_div = soup.select_one('#conts > div.wrap_dtl_atist > div > div.wrap_atist_info')

    # 아티스트 본명
    artist_info_dict['url_img_cover'] = soup.select_one('.wrap_dtl_atist .wrap_thumb #artistImgArea img').get('src')
    artist_info_dict['name'] = artist_simple_div.select_one('.title_atist').contents[1]

    # ==================== 상세 정보 ===================== #
    # 아티스트 소개

    if soup.select_one('#conts > div.section_atistinfo02'):
        artist_detail_introduce_div = soup.find('div', id='d_artist_intro')
        introduce_list = list()
        for item in artist_detail_introduce_div.contents:
            if item.name == 'br':
                introduce_list.append('\n')
            elif type(item) is Tag:
                introduce_list.append(item.string.strip())
            elif type(item) is NavigableString:
                introduce_list.append(item.strip())

        artist_detail_introduce = ''.join(introduce_list)
        artist_info_dict['intro'] = artist_detail_introduce

    # 아티스트 신상 정보
    artist_detail_normal_info = get_artist_dt_dd(soup, '#conts > div.section_atistinfo04 > dl')
    artist_info_dict['info'] = artist_detail_normal_info

    return artist_info_dict


def artist_search_from_melon_crawler(keyword):
    params = {
        'q': keyword,
    }
    soup = get_response(url=f'https://www.melon.com/search/artist/index.htm', params=params)

    artist_info_list = list()
    for artist_li in soup.select('#pageList > div > ul > li'):
        artist_name = artist_li.select_one('div > div > dl > dt > a').get_text()
        artist_url_image_cover = artist_li.select_one('div > a > img').get('src')
        artist_id = artist_li.select_one('div > div > dl > dd.wrap_btn > button')['data-artist-no']

        from artist.models import Artist
        artist_info_list.append({
            'artist_id': artist_id,
            'name': artist_name,
            'url_image_cover': artist_url_image_cover,
            'is_exist': Artist.objects.filter(melon_id=artist_id).exists(),
        })
    return artist_info_list
