from django.db import models


class Youtube(models.Model):
    video_id = models.CharField('Video ID', max_length=20, blank=True)
    channel_id = models.CharField('Channel ID', max_length=50, blank=True)
    title = models.CharField('제목', max_length=100, blank=True)
    channel_title = models.CharField('채널', max_length=20, blank=True)
    description = models.TextField('설명', blank=True)
    img_thumbnail = models.ImageField('썸네일', upload_to='youtube', blank=True, null=True)

    def __str__(self):
        return self.title
