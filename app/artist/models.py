from datetime import datetime

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.db import models

from crawler import get_artist_detail_crawler
from utils import *


def dynamic_profile_img_path(instance, filename):
    return f'artist/{instance.name}-{instance.melon_id}/{filename}'


class ArtistManager(models.Manager):
    def update_or_create_from_melon(self, artist_id):
        try:
            artist_info_dict = get_artist_detail_crawler(artist_id)
        except Exception as e:
            print(e)
        else:
            name = artist_info_dict.setdefault('name', '')
            # m = re.search('.*?.jpg|.png|.gif[/?]', artist_info_dict['url_img_cover'])
            # if m:
            #     url_img_cover = m.group()
            url_img_cover = artist_info_dict.setdefault('url_img_cover', '')
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

            birth_date = get_valid_date(birth_date)

            artist, created = self.update_or_create(
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

            temp_file = download(url_img_cover)
            file_name = '{artist_id}.{ext}'.format(
                artist_id=artist_id,
                ext=get_buffer_ext(temp_file)
            )
            if artist.img_profile:
                artist.img_profile.delete()
            artist.img_profile.save(file_name, File(temp_file))

            return artist, created


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


class ArtistLike(models.Model):
    # Artist와 User(members.User)와의 관계를 나타내는 중개 모델
    artist = models.ForeignKey(Artist, related_name='like_user_info_list', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='like_artist_info_list', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('artist', 'user'),
        )

    def __str__(self):
        return '"ArtistLike (User: {user}, Artist: {artist} Created: {created})'.format(
            user=self.user.username,
            artist=self.artist.name,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )
