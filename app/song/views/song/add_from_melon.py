from datetime import datetime

import requests

from django.core.files.base import ContentFile
from django.shortcuts import redirect

from ...models import Album
from ...models import Song
from crawler import *

__all__ = [
    'song_add_from_melon',
]


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
            album_id = song_info_dict.setdefault('album_id', '')
            album_info = album_detail_crawler(album_id)

            album, created = Album.objects.get_or_create(
                album_id=album_id,
                defaults={
                    'title':album_info['album_title'],
                    'release_date': datetime.strptime(album_info['release_date'], '%Y.%m.%d')
                }
            )
            url_img_cover = album_info['album_cover_img_url'].rsplit('.jpg', 1)[0] + '.jpg'
            response = requests.get(url_img_cover)
            binary_data = response.content

            from pathlib import Path
            file_name = Path(url_img_cover).name
            album.img_cover.save(file_name, ContentFile(binary_data))

            song, created = Song.objects.update_or_create(
                melon_id=song_id,
                defaults={
                    'title': song_info_dict.setdefault('title', ''),
                    'genre': song_info_dict.setdefault('genre', ''),
                    'lyrics': song_info_dict.setdefault('lyrics', ''),
                    'album': album,
                }
            )

            url_img_cover = song_info_dict.setdefault('url_image_cover', '').rsplit('.jpg', 1)[0] + '.jpg'
            response = requests.get(url_img_cover)
            binary_data = response.content

            from pathlib import Path
            file_name = Path(url_img_cover).name
            song.img_profile.save(file_name, ContentFile(binary_data))

        finally:
            return redirect('song:song-list')
