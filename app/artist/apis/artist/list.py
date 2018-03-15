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
                'name': artist.name
            }
            for artist in artists)
    }
    # return HttpResponse(json.dumps(data), content_type='application/json')
    return JsonResponse(data)

    # data = {
    #     'artists': json.dumps([dict(artist) for artist in artists.values('melon_id', 'name')]),
    # }
    # return HttpResponse(data)

# artist/       -> artist.urls.views
# api/artist/   -> artist.urls.apis
