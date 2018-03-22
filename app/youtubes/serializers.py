from rest_framework import serializers

from .models import Youtube


class YouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = '__all__'
