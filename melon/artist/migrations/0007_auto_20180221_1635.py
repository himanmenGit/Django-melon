# Generated by Django 2.0.2 on 2018-02-21 07:35

import artist.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_auto_20180220_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to=artist.models.dynamic_profile_img_path, verbose_name='프로필 이미지'),
        ),
    ]
