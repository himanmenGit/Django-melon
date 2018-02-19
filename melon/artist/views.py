from django.shortcuts import render, redirect
from django.utils import timezone

from artist.models import Artist


def artist_list(request):
    # 전체 Artist목록을 ul > li로 출력
    # 템플릿은 'artist/list.html'을 사용
    # 전달할 context키는 'artists'를 사용
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(request, 'artist/artist_list.html', context)


def artist_add(request):
    # HTML에 Artist클래스가 받을 수 있는 모든 input 구현
    # img_profile은 제외
    # method가 POST면 request.POST에서 해당 데이터 처리
    #   새 Artist객체를 만들고 artist_list로 이동
    # method가 GET이면 artist_add.html을 표시
    context = {

    }
    if request.method == 'POST':
        name = request.POST['artist_name']
        realname = request.POST['realname']
        nationality = request.POST['nationality']
        birth_date = request.POST['birth_date']
        constellation = request.POST['constellation']
        blood_type = request.POST['blood_type']
        intro = request.POST['intro']

        Artist.objects.create(
            name=name,
            real_name=realname,
            nationality=nationality,
            birth_date=birth_date,
            constellation=constellation,
            blood_type=blood_type,
            intro=intro,
        )
        return redirect('artists:artist-list')
    return render(request, 'artist/artist_add.html', context)
