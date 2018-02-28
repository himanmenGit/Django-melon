import requests
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from youtubes.models import Youtube
from ...models import Artist

__all__ = (
    'artist_detail',
)


def get_artist_youtube_detail(response):
    youtube_item_list = list()
    for item in response.get('items'):
        youtube_item_dict = dict()

        etag = item.get('etag')
        if etag:
            youtube_item_dict['etag'] = item.get('etag')
            youtube_item_dict['video_id'] = item.get('id').get('videoId', '')
            youtube_item_dict['channelId'] = item.get('snippet').get('channelId', '')
            youtube_item_dict['title'] = item.get('snippet').get('title', '')
            youtube_item_dict['description'] = item.get('snippet').get('description', '')
            youtube_item_dict['channel_title'] = item.get('snippet').get('channelTitle', '')
            youtube_item_dict['img_thumbnail'] = item.get('snippet').get('thumbnails').get('high').get('url', '')

            youtube = Youtube.objects.filter(etag=etag)
            if not youtube:
                youtube_item_list.append(youtube_item_dict)

    return youtube_item_list


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)

    # artist.name으로 유투브 검색
    # https://www.googleapis.com/youtube/v3/search?key=settings.YOUTUBE_API_KEY&part=snippet&q=artist.name

    url = 'https://www.googleapis.com/youtube/v3/search?'
    max_item = 5
    youtube_params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'q': artist.name,
        'maxResults': max_item,
        'type': 'video,channel'
    }
    youtube_list = get_artist_youtube_detail(requests.get(url, youtube_params).json())
    youtube_db_list = artist.like_youtube.all()
    context = {
        'artist': artist,
        'youtube_list': youtube_list,
        'youtube_db_list': youtube_db_list,
    }

    return render(request, 'artist/artist_detail.html', context)
