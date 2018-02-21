from collections import Counter

from django.db import models

from artist.models import Artist


class Album(models.Model):
    album_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    release_date = models.DateField('발매일')

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        return ', '.join(self.song_set.all().values_list('genre', flat=True).distinct())

    def __str__(self):
        # 호호호빵 [휘성, 김태우]
        # Merry & Happy [TWICE (트와이스)]
        # 이렇게 나오도록 작성
        #    전체 쿼리: self.artist.all()
        #       valeus_list
        return '{title} [{artists}]'.format(
            title=self.title,
            artists=', '.join(self.artists.values_list('name', flat=True))
        )
