# Generated by Django 2.0.2 on 2018-03-22 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img_profile_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
