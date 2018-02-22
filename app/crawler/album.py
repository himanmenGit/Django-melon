from .utils import *

__all__ = [
    'get_album_detail_crawler',
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
