import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from ...models import Artist

__all__ = (
    'artist_detail',
)


def get_artist_youtube_detail(response):
    youtube_item_list = list()
    for item in response.get('items'):
        youtube_item_dict = dict()

        video_channel_id = item.get('id').get('videoId', '')
        if video_channel_id:
            youtube_item_dict['video_id'] = video_channel_id
        else:
            video_channel_id = item.get('id').get('channelId', '')
            youtube_item_dict['channelId'] = video_channel_id

        youtube_item_dict['channelId'] = item.get('snippet').get('channelId', '')
        youtube_item_dict['title'] = item.get('snippet').get('title', '')
        youtube_item_dict['description'] = item.get('snippet').get('description', '')
        youtube_item_dict['channel_title'] = item.get('snippet').get('channelTitle', '')
        youtube_item_dict['img_thumbnail'] = item.get('snippet').get('thumbnails').get('high').get('url', '')

        # print('video_id:', youtube_item_dict.get('video_id'))
        # print('channelId:', youtube_item_dict.get('channelId'))
        # print('title:', youtube_item_dict.get('title'))
        # print('description', youtube_item_dict.get('description'))
        # print('channel_title', youtube_item_dict.get('channel_title'))
        # print('thumnail', youtube_item_dict.get('img_thumbnail'))

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
    }
    youtube_list = get_artist_youtube_detail(requests.get(url, youtube_params).json())

    context = {
        'artist': artist,
        'youtube_list': youtube_list,
    }

    return render(request, 'artist/artist_detail.html', context)
