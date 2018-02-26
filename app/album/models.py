from datetime import datetime

from django.conf import settings
from django.core.files.base import File
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
    release_date = models.DateField('발매일')

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        return ', '.join(self.song_set.all().values_list('genre', flat=True).distinct())

    objects = AlbumManager()

    like_users = models.ManyToManyField(
        # User,
        settings.AUTH_USER_MODEL,
        through='AlbumLike',
        related_name='like_albums',
        blank=True,
    )

    def __str__(self):
        return self.title

    def toggle_like_user(self, user):
        """
        자신의 like_users에 주어진 user가 존재 하지 않으면 like_users에 추가 한다.
        이미 존재할 경우에는 없앤다.

        :param user:
        :return:
        """
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created


class AlbumLike(models.Model):
    # Album와 User(members.User)와의 관계를 나타내는 중개 모델
    album = models.ForeignKey(Album, related_name='like_user_info_list', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='like_album_info_list', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('album', 'user'),
        )

    def __str__(self):
        return '"AlbumLike (User: {user}, Album: {album} Created: {created})'.format(
            user=self.user.username,
            album=self.title,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )
