import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect

User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    # code 로 부터 AccessToken 가져 오기
    params = dict()

    params['client_id'] = settings.FACEBOOK_APP_ID
    params['client_secret'] = settings.FACEBOOK_SECRET_CODE

    # 페이스북 로그인 버튼을 누른후, 사용자가 승인하면 redirect_uri 에 GET parameter로 'code' 가 전송됨
    # 이 값과 client_id, secret 을 사용해서 Facbook서버에서 access_token을 받아와야함.
    params['code'] = request.GET['code']

    # 이전에 페이스북 로그인 버튼을 눌렀을 때 'code'를 다시 전달받은 redirect_uri값을 그대로 사용
    params['redirect_uri'] = 'http://localhost:8000/facebook-login/'

    # 아래 엔드포인트에 GET요청을 보냄
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    response = requests.get(url, params=params)

    # requests.get이 response를 받아오는데 이는 페이스북에서 json형태의 문자열로 보냄
    # requsets.json() 을 이용하여 python의 dict객체로 만들어 줌.
    response_dict = response.json()
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    # GraphApu의 me 엔드포인트에 GET요청 보내기
    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ]),
    }
    response = requests.get(url, params=params)
    response_dict = response.json()

    '''
    {
        'id': '1956941341000445', 
        'name': '박수민', 
        'picture': 
            {
                'data': {
                    'height': 2048, 'is_silhouette': False,
                    'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/477538_428745627153365_1446182677_o.jpg?oh=840c6fb827ab4be0596643bbb5b4eb12&oe=5B02C4DE',
                    'width': 1536
                }
            },
        'first_name': '수민',
        'last_name': '박'
    }
    '''
    facebook_id = response_dict['id']
    facebook_name = response_dict['name']
    facebook_url_picture = response_dict['picture']['data']['url']
    facebook_first_name = response_dict['first_name']
    facebook_last_name = response_dict['last_name']

    # facebook_id가 username인 User가 존재할 경우
    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    # 존재하지 않으면 새 유저를 생성
    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=facebook_first_name,
            last_name=facebook_last_name,
        )
    # 해당 유저를 로그인 시킴
    login(request, user)
    return redirect('index')
