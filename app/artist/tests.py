import random

import math

import base64
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from io import BytesIO
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer
from rest_framework.test import APITestCase, APIClient

from artist.serializers import ArtistSerializer
from utils import get_buffer_ext
from utils.pagination import SmallPagination
from .models import Artist
from .apis import ArtistListCreateView


class ArtistListTest(APITestCase):
    MODEL = Artist
    VIEW = ArtistListCreateView
    PATH = '/api/artist/'
    VIEW_NAME = 'apis:artist:artist-list'
    PAGINATION_COUNT = SmallPagination.page_size

    def test_reverse(self):
        f"""
        Artist List에 해당하는 VIEW_NAME을 reverse한 결과가 기대 PATH와 같은지 검사
            VIEW_NAME:  {self.VIEW_NAME}
            PATH:       {self.PATH}
        :return:
        """

        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_resolve(self):
        f"""
        Artist List에 해당하는 PATH를 resolve한 결과의 func와 view_name이
        기대하는 View.as_view()와 VIEW_NAME과 같은지 검사
            PATH:       {self.PATH}
            VIEW_NAME:  {self.VIEW_NAME}
        :return:
        """

        resolver_match = resolve(self.PATH)

        self.assertEqual(resolver_match.func.__name__, self.VIEW.as_view().__name__)
        self.assertEqual(resolver_match.view_name, self.VIEW_NAME)

    def test_artist_list_count(self):
        num = random.randrange(10, 20)
        for i in range(num):
            Artist.objects.create(name=f'Artist{i}')

        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), self.MODEL.objects.count())
        self.assertEqual(response.data.get('count'), num)

    def test_artist_list_pagination(self):
        num = 13
        for i in range(num):
            Artist.objects.create(name=f'Artist{i + 1}')

        response = self.client.get(self.PATH, {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(math.ceil(num / self.PAGINATION_COUNT)):
            response = self.client.get(self.PATH, {'page': i + 1})
            self.assertLessEqual(len(response.data.get('results')), self.PAGINATION_COUNT)

            self.assertEqual(response.data.get('results'),
                             ArtistSerializer(Artist.objects.all()[i * 5:(i + 1) * 5], many=True).data, )


class ArtistCreateTest(APITestCase):
    PATH = '/api/artist/'

    def test_create_artist(self):
        # /static/test/suzi.jpg에 잇는 파일을 사용해서
        # 나머지 데이터를 채워서 Artist객체를 생성
        # 파일을 이진데이터로 읽어서 생성하면 됩니다.
        # 생성할 Artist의 '파일 필드 명' 으로 전당
        # self.client.post(URL, {'img_profile': <파일객체>})
        User = get_user_model()
        user = User.objects.create(
            username='himanmen'
        )

        from django.contrib.staticfiles import finders

        path = finders.find('test/suzi.jpg')

        images = ''
        with open(path, 'rb') as f:
            images = f.read()

        temp_file = BytesIO()
        temp_file.write(images)
        temp_file.seek(0)

        file_name = '{artist_id}.{ext}'.format(
            artist_id=123,
            ext=get_buffer_ext(temp_file)
        )

        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(self.PATH, {'name': '아이유','img_profile': File(temp_file, name=file_name)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data,
                         ArtistSerializer(Artist.objects.first()).data)
