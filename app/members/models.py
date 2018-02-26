from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def toggle_like_artist(self, artist):
        """
        자신의 like_artist에 주어진 artist가 존재 하지 않으면 like_artist에 추가 한다.
        이미 존재할 경우에는 없앤다.

        :param user, artist:
        :return:
        """
        # like_artist_list = self.like_artist_info_list
        # like_artist = like_artist_list.filter(artist=artist)
        # if like_artist.exists():
        #     like_artist.delete()
        #     return True
        # else:
        #     like_artist_list.create(artist=artist)
        #     return False

        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created
