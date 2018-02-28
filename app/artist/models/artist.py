from django.conf import settings
from django.db import models

from .manager import ArtistManager
from youtubes.models import Youtube

__all__ = (
    'Artist',
)


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = 'x'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )
    melon_id = models.CharField('멜론 Artist ID', max_length=20, blank=True, null=True, unique=True)
    img_profile = models.ImageField('프로필 이미지', upload_to='artist', blank=True)
    name = models.CharField('이름', max_length=50)
    real_name = models.CharField('본명', max_length=50, blank=True)
    nationality = models.CharField('국적', max_length=50, blank=True)
    birth_date = models.DateField('생년월일', blank=True, null=True)
    constellation = models.CharField('별자리', max_length=30, blank=True, null=True)
    blood_type = models.CharField('혈액형', max_length=30, choices=CHOICES_BLOOD_TYPE, blank=True)
    intro = models.TextField('소개', blank=True)

    like_users = models.ManyToManyField(
        # User,
        settings.AUTH_USER_MODEL,
        through='ArtistLike',
        related_name='like_artists',
        blank=True,
    )

    like_youtube = models.ManyToManyField(
        # Youtube,
        Youtube,
        through='YoutubeLike',
        related_name='like_youtube',
        blank=True,
    )

    objects = ArtistManager()

    def __str__(self):
        return self.name

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
