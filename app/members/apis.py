from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer


class AuthTokenView(APIView):
    def post(self, request):
        # URL: /api/members/auth-token/
        # username, password를 받음
        # 유저 인증에 성공했을 경우
        # 토큰을 생성하거나 있으면 존재하는걸 가져와서
        # Response로 돌려줌
        # username = request.data.get('username')
        # password = request.data.get('password')
        # user = authenticate(username=username, password=password)

        serializer = AuthTokenSerializer(data=request.data)
        user = serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class MyUserDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        print(request.user)
        serializer = UserSerializer(request.user)
        data = {
            'user': serializer.data
        }
        return Response(data)
