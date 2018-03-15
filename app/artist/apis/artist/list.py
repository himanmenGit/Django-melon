import json

from django.http import JsonResponse, HttpResponse

from artist.models import Artist

__all__ = (
    'artist_list',
)


def artist_list(reqeust):
    """
    data: {
        ''artists': {
            {
                'melon_id': ...
                'name': ...,
            },
            {
                'melon_id': ...
                'name': ...,
            },
            ...
        }
    }
    :param reqeust:
    :return:
    """
    # localhost:8000/api/artist/
    artists = Artist.objects.all()
    data = {
        'artists': list(
            {
                'melon_id': artist.melon_id,
                'name': artist.name,
                'img_profile': artist.img_profile.url,
            }
            for artist in artists)
    }

    return JsonResponse(data)

# artist/       -> artist.urls.views
# api/artist/   -> artist.urls.apis
