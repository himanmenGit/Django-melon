from django.db import models


# 내가 한거
# from album.models import Album
# from artist.models import Artist
#
#
# class Song(models.Model):
#     title = models.CharField('제목', max_length=100)
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     is_title = models.BooleanField('타이틀곡입니까', default=False)

# 클래스 매니저님
# Artist
#   - Album
#       - Song
#       - Song
#       - Song
#       - Song
# from album.models import Album
# from artist.models import Artist
#
#
# class Song(models.Model):
#     title = models.CharField('제목', max_length=255)
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)
#     artist = models.ManyToManyField(Artist, through='ArtistSong', related_name='+')
#
#     def __str__(self):
#         return self.title
#
#
# class ArtistSong(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     demo_date = models.DateTimeField()
#
#     def __str__(self):
#         return f'{self.artist.name} {self.song.title} '
from album.models import Album


class Song(models.Model):
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.CharField('곡 제목', max_length=100)
    genre = models.CharField('장르', max_length=100, blank=True, null=True)
    lyrics = models.TextField('가사', blank=True)

    @property
    def artists(self):
        # self.album에 속한 전체 Artist의 QuerySet리턴
        return self.album.artists.all()

    @property
    def release_date(self):
        # self.album의 release_date를 리턴
        return self.album.release_date

    @property
    def formatted_release_date(self):
        # 2017.01.15
        return self.release_date.strftime('%Y.%m.%d')

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        # TWICE (트와이스) - Heart Shaker (Merry & Happy)
        return '{artists} - {title} ({album})'.format(
            artists=', '.join(self.album.artists.values_list('name', flat=True)),
            title=self.title,
            album=self.album.title,
        )
