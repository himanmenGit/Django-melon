from django.db import models

from artist.models import Artist


# 내가 한거
# class Album(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     title = models.CharField('앨범명', max_length=100, blank=True)
#     release_date = models.DateField('출시일', 'Release Date')
#     # genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
#     publisher = models.CharField('소속사', max_length=50, blank=True)
#     agency = models.CharField('기획사', max_length=50, blank=True)
#     intro = models.TextField('앨범소개', blank=True)

# 클래스 매니저님
# # Album
# #   - Song
# #   - Song
# #   - Song
# #   - Song
#
# class Album(models.Model):
#     title = models.CharField('앨범명', max_length=255)  # 앨범 제목
#     artist = models.ManyToManyField(Artist)
#
#     def __str__(self):
#         return self.title

class Album(models.Model):
    title = models.CharField(max_length=100)
    img_cover = models.ImageField('커버 이미지', upload_to='album', blank=True)
    artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    release_date = models.DateField('발매일')

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        return ''

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
