from .artist import *
from .artist_like import *
from .artist_youtube import *


def dynamic_profile_img_path(instance, filename):
    return f'artist/{instance.name}-{instance.melon_id}/{filename}'
