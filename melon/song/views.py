from django.shortcuts import render

from .models import Song


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    return render(request, 'song/song_list.html', context)


def song_search(request):
    """
    사용할 URL: song/search/
    사용할 Template: templates/song/song_search.html
        form 안에
            input한개, button한개 배치
    1. song/urls.py에 URL작성
    2. templates/song/song_search.thml작성
        {% extends %} 사용할 것
        form 배치후 method는 POST, {% csrf_token %}배치
    3. 이 함수에서 return render(...)
        * 아직 context는 사용하지 않음

    - 검색 구현
    1. input의 name을 keyword로 지정
    2. 이 함수를 request.method 가 'GET'일 때와 'POST"일 때로 분기
    3. request.method가 'POST'일 때
        request.POST dict의 'name'키에 해당하는 값을
        HttpResponse로 출력
    4. request.method가 'GET' 일 떄 이전에 하던 템플릿 출력을 유지

    - Query filter로 검색하기
    1. keyword가 자신의 'title'에 포함되는 Song쿼리 셋 생성
    2. 위 쿼리셋을 'songs'변수에 할당
    3. context dict를 만들고 'songs'키에 songs변수를 할당
    4. render의 3번쨰 인수로 context를 전달
    5. template에 전달된 'songs'를 출력


    # songs_from_artists
    # songs_from_albums
    # song_from_title
    # 위 세 변수에 더 위의 조건 3개에 부합하는 쿼리셋을 각각 전달
    #  세 변수를 이용해 검색 결과를 3단으로 분리해서 출력

    :param request:
    :return:
    """
    context = dict()
    try:
        keyword = request.GET['keyword'].strip()
    except KeyError as e:
        print('KeyError 에러 발생!', e)
        keyword = None;

    if keyword:
        songs_from_artists = Song.objects.filter(album__artists__name__contains=keyword)
        songs_from_albums = Song.objects.filter(album__title__contains=keyword)
        songs_from_title = Song.objects.filter(title__contains=keyword)
        context['songs_from_artists'] = songs_from_artists
        context['songs_from_albums'] = songs_from_albums
        context['songs_from_title'] = songs_from_title
    return render(request, 'song/song_search.html', context)
