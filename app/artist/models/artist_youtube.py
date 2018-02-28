from datetime import datetime
from django.db import models

from .artist import Artist
from youtubes.models import Youtube

__all__ = (
    'YoutubeLike',
)


class YoutubeLike(models.Model):
    artist = models.ForeignKey(Artist, related_name='like_youtube_artist_info_list', on_delete=models.CASCADE)
    youtube = models.ForeignKey(Youtube, related_name='like_youtube_info_list', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('artist', 'youtube'),
        )

    def __str__(self):
        return '"YoutubeLike (Artist: {artist}, Youtube: {youtube} Created: {created})'.format(
            artist=self.artist.name,
            youtube=self.youtube.title,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )
