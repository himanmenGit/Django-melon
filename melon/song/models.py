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


class Song(models.Model):
    pass