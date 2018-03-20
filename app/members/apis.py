from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

User = get_user_model()


class AuthTokenView(APIView):
    def post(self, request):
        # URL: /api/members/auth-token/
        # username, password를 받음
        # 유저 인증에 성공했을 경우
        # 토큰을 생성하거나 있으면 존재하는걸 가져와서
        # Response로 돌려줌
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        token = Token.objects.get_or_create(user=user)
        print(token)
        return Response(str(token))
