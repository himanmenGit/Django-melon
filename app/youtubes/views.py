from django.core.files import File
from django.shortcuts import render, redirect

from artist.models import Artist
from utils import download, get_buffer_ext
from .models import Youtube


def youtube_add(request):
    print('etag ', request.POST['etag'])
    print('video ', request.POST['video_id'])
    print('channel ', request.POST['channel_id'])
    print('title ', request.POST['title'])
    print('c_title ', request.POST['channel_title'])
    print('des ', request.POST['description'])
    print('url ', request.POST['img_thumbnail'])
    print('artist_pk ', request.POST['artist_pk'])

    etag = request.POST.get('etag', '')
    video_id = request.POST.get('video_id', '')
    channel_id = request.POST.get('channel_id', '')
    title = request.POST.get('title', '')
    channel_title = request.POST.get('channel_title', '')
    description = request.POST.get('description', '')
    url_img_thumbnail = request.POST.get('img_thumbnail', '')
    artist_pk = request.POST.get('artist_pk', '')

    youtube = Youtube.objects.create(
        etag=etag,
        video_id=video_id,
        channel_id=channel_id,
        title=title,
        channel_title=channel_title,
        description=description,
    )

    temp_file = download(url_img_thumbnail)
    file_name = '{video_id}.{ext}'.format(
        video_id=video_id,
        ext=get_buffer_ext(temp_file)
    )
    if youtube.img_thumbnail:
        youtube.img_thumbnail.delete()
    youtube.img_thumbnail.save(file_name, File(temp_file))

    youtube.like_youtube_info_list.create(
        artist=Artist.objects.get(pk=artist_pk)
    )
    return redirect('artist:artist-detail', artist_pk=artist_pk)
