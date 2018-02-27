from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)

    def toggle_like_artist(self, artist):
        """
        자신의 like_artist에 주어진 artist가 존재 하지 않으면 like_artist에 추가 한다.
        이미 존재할 경우에는 없앤다.

        :param user, artist:
        :return:
        """
        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created

    def toggle_like_song(self, song):
        like, like_created = self.like_song_info_list.get_or_create(song=song)
        if not like_created:
            like.delete()
        return like_created

    def toggle_like_album(self, album):
        like, like_created = self.like_album_info_list.get_or_create(album=album)
        if not like_created:
            like.delete()
        return like_created
