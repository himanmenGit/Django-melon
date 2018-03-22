import requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'img_profile_url',
        )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        if access_token:
            user = authenticate(access_token=access_token)
            if not user:
                raise serializers.ValidationError('액세스 토큰이 올바르지 않습니다.')
        else:
            raise serializers.ValidationError('액세스 토큰이 ..')

        attrs['user'] = user
        return attrs
