from datetime import datetime

import requests

from django.core.files.base import ContentFile
from django.shortcuts import redirect

from artist.models import Artist
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
        Song.objects.update_or_create_from_melon(request.POST['song_id'])
        return redirect('song:song-list')
