from rest_framework import serializers

from members.serializers import UserSerializer
from youtubes.serializers import YouTubeSerializer
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(many=True, read_only=True)
    like_youtube = YouTubeSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = (
            'pk',
            'name',
            'img_profile',

            'like_users',
            'like_youtube',
        )
