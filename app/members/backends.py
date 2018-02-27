import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File

from utils import download, get_buffer_ext

User = get_user_model()


class FacebookBackend:
    CLIENT_ID = settings.FACEBOOK_APP_ID
    CLIENT_SECRET = settings.FACEBOOK_SECRET_CODE
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'
    URL_ME = 'https://graph.facebook.com/v2.12/me'

    def authenticate(self, request, code):
        def get_access_token(auth_code):
            """
            유저가 페이스북에서 우리 애플리케이션의 사용에 대해 '승인' 한 경우,
            페이스북에서 우리 애플리케이션의 주소(redirect_uri)에 'code'라는 GET parameter로 전해주는
            인증 코드 (auth_code)를 사용해서
            페이스북 GraphApi에 access_token요청, 결과를 가져와 리턴

            :param auth_code: 유저가 페이스북에 로그인/앱 승인한 결과로 돌아오는 'code' GET parameter
            :return: access_token
            """
            redirect_uri = 'http://localhost:8000/facebook-login/'
            # 아래 엔드포인트에 GET요청을 보냄
            params_access_token = {
                'client_id': self.CLIENT_ID,
                'redirect_uri': redirect_uri,
                'client_secret': self.CLIENT_SECRET,
                'code': auth_code,
            }

            response = requests.get(self.URL_ACCESS_TOKEN, params=params_access_token)
            # 결과는 JSON 문자열 JSON 디코더를 이용하여 DICT로 변환
            response_dict = response.json()
            return response_dict['access_token']

        def get_user_info(user_access_token):
            """
            User access token을 사용해서
            GraphAPI의 'User' 항목을 리턴
                (엔드포인트 'me'를 사용해서 access_token에 해당하는 사용자의 정보를 가져옴)
            :param user_access_token: 정보를 가져올 Facebook User access token
            :return: User정보 (dict)
            """
            params_user = {
                'access_token': user_access_token,
                'fields': ','.join([
                    'id',
                    'name',
                    'picture.width(2500)',
                    'first_name',
                    'last_name',
                ]),
            }
            response = requests.get(self.URL_ME, params=params_user)
            response_dict = response.json()
            return response_dict

        try:
            access_token = get_access_token(code)
            user_info = get_user_info(access_token)
            facebook_id = user_info['id']
            facebook_name = user_info['name']
            facebook_url_picture = user_info['picture']['data']['url']
            facebook_first_name = user_info['first_name']
            facebook_last_name = user_info['last_name']

            try:
                user = User.objects.get(username=facebook_id)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=facebook_id,
                    first_name=facebook_first_name,
                    last_name=facebook_last_name,
                )

                temp_file = download(facebook_url_picture)
                file_name = '{facebook_id}.{ext}'.format(
                    facebook_id=facebook_id,
                    ext=get_buffer_ext(temp_file)
                )
                if user.img_profile:
                    user.img_profile.delete()
                user.img_profile.save(file_name, File(temp_file))

            return user
        except Exception as e:
            print(e)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
