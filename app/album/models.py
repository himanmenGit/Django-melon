import re
from datetime import date
from django.core.files.base import ContentFile, File
from django.db import models

from crawler import get_album_detail_crawler
from utils import *


class AlbumManager(models.Manager):
    def update_or_create_from_melon(self, album_id):
        try:
            album_info = get_album_detail_crawler(album_id)
        except Exception as e:
            print(e)
        else:
            # album 추가
            url_img_cover = album_info.setdefault('album_cover_img_url', '')
            release_date = get_valid_date(album_info.setdefault('release_date', ''))

            album, created = Album.objects.get_or_create(
                album_id=album_id,
                defaults={
                    'title': album_info['album_title'],
                    'release_date': release_date,
                }
            )

            temp_file = download(url_img_cover)
            file_name = '{album_id}.{ext}'.format(
                album_id=album_id,
                ext=get_buffer_ext(temp_file)
            )
            album.img_cover.save(file_name, File(temp_file))

            return album, created


class Album(models.Model):
    album_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    # artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    release_date = models.DateField('발매일')

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        return ', '.join(self.song_set.all().values_list('genre', flat=True).distinct())

    objects = AlbumManager()

    def __str__(self):
        # 호호호빵 [휘성, 김태우]
        # Merry & Happy [TWICE (트와이스)]
        # 이렇게 나오도록 작성
        #    전체 쿼리: self.artist.all()
        #       valeus_list
        # return '{title} [{artists}]'.format(
        #     title=self.title,
        #     artists=', '.join(self.artists.values_list('name', flat=True))
        # )
        return self.title
