from rest_framework import serializers

from .models import Youtube


class ArtistYouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = '__all__'
