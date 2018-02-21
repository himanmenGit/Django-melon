import requests
from bs4 import NavigableString

from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from io import BytesIO

from crawler import *
from ...models import Song

__all__ = [
    'song_add_from_melon',
]


# def get_detail(song_id):
#     params = {
#         'songId': song_id
#     }
#
#     soup = get_response(url=f'https://www.melon.com/song/detail.htm', params=params)
#
#     if not soup:
#         return
#
#     song_info_dict = dict()
#
#     div_entry = soup.find('div', class_='entry')
#
#     dl = div_entry.find('div', class_='meta').find('dl')
#     items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
#     it = iter(items)
#     description_dict = dict(zip(it, it))
#     song_info_dict['album'] = description_dict.get('앨범')
#     song_info_dict['release_date'] = description_dict.get('발매일')
#     song_info_dict['genre'] = description_dict.get('장르')
#
#     song_info_dict['title'] = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
#     song_info_dict['artist'] = div_entry.find('div', class_='artist').get_text()
#     artist_a = div_entry.find('div', class_='artist').find('a')
#     if artist_a:
#         song_info_dict['artist'] = artist_a.find('span').get_text()
#
#     div_lyrics = soup.find('div', id='d_video_summary')
#     if div_lyrics:
#         lyrics_list = list()
#         for item in div_lyrics.contents:
#             if item.name == 'br':
#                 lyrics_list.append('\n')
#             elif type(item) is NavigableString:
#                 lyrics_list.append(item.strip())
#
#         song_info_dict['lyrics'] = ''.join(lyrics_list)
#
#     song_info_dict['url_image_cover'] = soup.select_one('#downloadfrm > div > div > div.thumb > a > img').get('src')
#
#     return song_info_dict


def song_add_from_melon(request):
    # artist_add_from_melon과 같은 기능을 함.
    #   song_search_from_melon도 구현
    #       -> 이 안에 'DB에 추가' 하는 Form구현

    # 데이터 추가
    if request.method == 'POST':
        try:
            song_id = request.POST['song_id']
            song_info_dict = get_song_detail_crawler(song_id)
        except Exception as e:
            print(e)
        else:
            # album = song_info_dict.get.setdefault('album', '')
            # release_date = song_info_dict.setdefault('release_date', '')
            genre = song_info_dict.setdefault('genre', '')
            title = song_info_dict.setdefault('title', '')
            # artist = song_info_dict.setdefault('artist', '')
            lyrics = song_info_dict.setdefault('lyrics', '')
            url_img_cover = song_info_dict.setdefault('url_image_cover', '').rsplit('.jpg', 1)[0] + '.jpg'

            # if release_date:
            #     release_date = datetime.strptime(release_date, '%Y.%m.%d')
            # else:
            #     release_date = datetime.now().strftime('%Y-%m-%d')

            response = requests.get(url_img_cover)
            binary_data = response.content
            # temp_file = BytesIO()
            # temp_file.write(binary_data)
            # temp_file.seek(0)

            song, created = Song.objects.update_or_create(
                melon_id=song_id,
                defaults={
                    'title': title,
                    'genre': genre,
                    'lyrics': lyrics,
                }
            )

            from pathlib import Path
            file_name = Path(url_img_cover).name
            song.img_profile.save(file_name, ContentFile(binary_data))

        finally:
            return redirect('song:song-list')
