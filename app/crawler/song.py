import re
from bs4 import NavigableString

from .utils import *

__all__ = [
    'song_search_from_melon_crawler',
    'get_song_detail_crawler',
]


def get_song_detail_crawler(song_id):
    params = {
        'songId': song_id
    }

    soup = get_response(url=f'https://www.melon.com/song/detail.htm', params=params)

    if not soup:
        return

    song_info_dict = dict()

    div_entry = soup.find('div', class_='entry')

    dl = div_entry.find('div', class_='meta').find('dl')
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))
    song_info_dict['album'] = description_dict.get('앨범')
    song_info_dict['release_date'] = description_dict.get('발매일')
    song_info_dict['genre'] = description_dict.get('장르')

    song_info_dict['title'] = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
    artist_a = div_entry.find('div', class_='artist').find('a')
    if artist_a:
        song_info_dict['artist'] = artist_a.find('span').get_text()

        # downloadfrm > div > div > div.entry > div.info > div.artist > a

        p = re.compile(r'javascript:melon.link.goArtistDetail[(]\'(\d+)\'[)]')
        artist_id = p.search(str(artist_a)).group(1)
        song_info_dict['artist_id'] = artist_id

    div_lyrics = soup.find('div', id='d_video_summary')
    if div_lyrics:
        lyrics_list = list()
        for item in div_lyrics.contents:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())

        song_info_dict['lyrics'] = ''.join(lyrics_list)

    p = re.compile(r'javascript:melon.link.goAlbumDetail[(]\'(\d+)\'[)]')
    album_id = p.search(str(dl)).group(1)
    song_info_dict['album_id'] = album_id

    song_info_dict['url_image_cover'] = soup.select_one('#downloadfrm > div > div > div.thumb > a > img').get('src')

    return song_info_dict


def song_search_from_melon_crawler(keyword):
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

        from song.models import Song
        song_info_list.append({
            'song_id': song_id,
            'title': title,
            'artist': artist,
            'album': album,
            'is_exist': Song.objects.filter(melon_id=song_id).exists(),
        })
    return song_info_list
