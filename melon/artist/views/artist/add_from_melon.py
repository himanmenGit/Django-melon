import requests
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from datetime import datetime

from crawler import *
from ...models import Artist

__all__ = [
    'artist_add_from_melon',
]


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
        try:
            artist_id = request.POST['artist_id']
            artist_info_dict = get_artist_detail_crawler(artist_id)
            artist_name = request.POST['artist_name']
            artist_url_image_cover = request.POST['artist_url_image_cover']
        except Exception as e:
            print(e)
        else:
            name = artist_name
            url_img_cover = artist_url_image_cover.rsplit('.jpg', 1)[0] + '.jpg'
            real_name = artist_info_dict['info'].setdefault('본명', '')
            nationality = artist_info_dict['info'].setdefault('국적', '')
            birth_date = artist_info_dict['info'].setdefault('생일', '')
            constellation = artist_info_dict['info'].setdefault('별자리', '')
            blood_type = artist_info_dict['info'].setdefault('혈액형', '')
            intro = artist_info_dict.setdefault('intro', '')

            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if blood_type.strip() == full:
                    blood_type = short
                    break
            else:
                blood_type = Artist.BLOOD_TYPE_OTHER

            if birth_date:
                birth_date = datetime.strptime(birth_date, '%Y.%m.%d')
            else:
                birth_date = None;

            response = requests.get(url_img_cover)
            binary_data = response.content

            artist, created = Artist.objects.update_or_create(
                melon_id=artist_id,
                defaults={
                    'name': name,
                    'real_name': real_name,
                    'nationality': nationality,
                    'birth_date': birth_date,
                    'constellation': constellation,
                    'blood_type': blood_type,
                    'intro': intro,
                }
            )

            from pathlib import Path
            file_name = Path(url_img_cover).name
            artist.img_profile.save(file_name, ContentFile(binary_data))
        finally:
            return redirect('artist:artist-list')
