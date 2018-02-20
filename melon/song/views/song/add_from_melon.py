from django.shortcuts import redirect

__all__ = [
    'song_add_from_melon',
]


def song_add_from_melon(request):
    # artist_add_from_melon과 같은 기능을 함.
    #   song_search_from_melon도 구현
    #       -> 이 안에 'DB에 추가' 하는 Form구현

    # 데이터 추가
    return redirect('song:song-list')
