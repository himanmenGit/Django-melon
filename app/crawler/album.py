from .utils import *

__all__ = [
    'get_album_detail_crawler',
    'album_search_from_melon_crawler',
]


def get_album_detail_crawler(album_id):
    params = {
        'albumId': album_id
    }

    soup = get_response(url=f'https://www.melon.com/album/detail.htm', params=params)

    if not soup:
        return

    album_title = soup.find('div', class_="song_name").strong.next_sibling.strip()
    album_cover_img_url = soup.find('a', id='d_album_org').img.get('src')

    div_entry = soup.find('div', class_='entry')
    dl = div_entry.find('div', class_='meta').find('dl')
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))

    album_release_date = description_dict.get('발매일')

    result_dict = dict()
    result_dict['album_title'] = album_title
    result_dict['album_cover_img_url'] = album_cover_img_url
    result_dict['release_date'] = album_release_date

    return result_dict


def album_search_from_melon_crawler(keyword):
    params = {
        'q': keyword,
    }
    soup = get_response(url=f'https://www.melon.com/search/album/index.htm', params=params)

    album_info_list = list()
    for album_li in soup.select('#frm > div > ul > li'):
        album_title = album_li.select_one('div > div > dl > dt > a').get_text()
        album_url_image_cover = album_li.select_one('div > a > img').get('src')
        album_id = album_li.select_one('div > div > dl > dd.wrap_btn > a')['data-album-no']

        from album.models import Album
        album_info_list.append({
            'album_id': album_id,
            'album_title': album_title,
            'url_image_cover': album_url_image_cover,
            'is_exist': Album.objects.filter(album_id=album_id).exists(),
        })
    return album_info_list
