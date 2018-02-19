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
    :param request:
    :return:
    """
    context = {

    }

    return render(request, 'song/song_search.html', context)
