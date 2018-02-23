from django.core.files.base import ContentFile, File
from django.db import models

from album.models import Album
from artist.models import Artist
from crawler import get_song_detail_crawler
from utils import *


class SongManager(models.Manager):
    def update_or_create_from_melon(self, song_id):
        """
        song_id에 해당하는 Song 정보를 멜론사이트에서 가져와 update_or_create를 실행
        이 때, 해당 Song의 Artist정보도 가져와 ArtistManaget.update_or_create_from_melon도 실행
            그리고 해당 Song의 Album정보도 가져와서 AlbumManager.update_or_create_from_melon도 실행
        :param song_id: 멜론 사이트에서의 곡 고유 ID
        :return: (Song instance, Bool(Song created))
        """
        try:
            song_info_dict = get_song_detail_crawler(song_id)
        except Exception as e:
            print(e)
        else:
            # artist 추가
            artist_id = song_info_dict.setdefault('artist_id', '')
            artist, created = Artist.objects.update_or_create_from_melon(artist_id)

            album_id = song_info_dict.setdefault('album_id', '')
            album, created = Album.objects.update_or_create_from_melon(album_id)

            # song 추가
            song, created = Song.objects.update_or_create(
                melon_id=song_id,
                defaults={
                    'title': song_info_dict.setdefault('title', ''),
                    'genre': song_info_dict.setdefault('genre', ''),
                    'lyrics': song_info_dict.setdefault('lyrics', ''),
                    'album': album,
                }
            )

            url_img_cover = song_info_dict.setdefault('url_image_cover', '')
            temp_file = download(url_img_cover)
            file_name = '{song_id}.{ext}'.format(
                song_id=song_id,
                ext=get_buffer_ext(temp_file)
            )
            song.img_profile.save(file_name, File(temp_file))

            song.artists.add(artist)

            return song, created


class Song(models.Model):
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )
    melon_id = models.CharField('멜론 Song ID', max_length=20, blank=True, null=True, unique=True)
    img_profile = models.ImageField('프로필 이미지', upload_to='song', blank=True)
    title = models.CharField('곡 제목', max_length=100)
    genre = models.CharField('장르', max_length=100, blank=True, null=True)
    lyrics = models.TextField('가사', blank=True)

    @property
    def release_date(self):
        # self.album의 release_date를 리턴
        return self.album.release_date

    @property
    def formatted_release_date(self):
        # 2017.01.15
        return self.release_date.strftime('%Y.%m.%d')

    objects = SongManager()

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        # TWICE (트와이스) - Heart Shaker (Merry & Happy)

        return '{artists} {title} ({album})'.format(
            artists=', '.join(self.artists.values_list('name', flat=True)),
            title=self.title,
            album=self.album.title,
        )
