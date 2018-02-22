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
        Artist.objects.update_or_create_from_melon(request.POST['artist_id'])
        return redirect('artist:artist-list')
