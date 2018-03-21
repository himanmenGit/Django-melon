from rest_framework import serializers

from members.serializer import UserSerializer
from youtubes.serializers import ArtistYouTubeSerializer
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(
        many=True,
        read_only=True,
    )
    like_youtube = ArtistYouTubeSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Artist
        fields = '__all__'
