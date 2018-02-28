from django.core.files import File
from django.db import models

from crawler import get_artist_detail_crawler
from utils import download, get_buffer_ext, get_valid_date

__all__ = (
    'ArtistManager',
)


class ArtistManager(models.Manager):
    def update_or_create_from_melon(self, artist_id):
        try:
            artist_info_dict = get_artist_detail_crawler(artist_id)
        except Exception as e:
            print(e)
        else:
            from ..models.artist import Artist

            name = artist_info_dict.setdefault('name', '')
            # m = re.search('.*?.jpg|.png|.gif[/?]', artist_info_dict['url_img_cover'])
            # if m:
            #     url_img_cover = m.group()
            url_img_cover = artist_info_dict.setdefault('url_img_cover', '')
            real_name = artist_info_dict['info'].setdefault('본명', '')
            nationality = artist_info_dict['info'].setdefault('국적', '')
            birth_date = artist_info_dict['info'].setdefault('생일', '')
            constellation = artist_info_dict['info'].setdefault('별자리', '')
            blood_type = artist_info_dict['info'].setdefault('혈액형', '')
            intro = artist_info_dict.setdefault('intro', '')

            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if blood_type.strip() == full:
                    blood_type = short
                    break
            else:
                blood_type = Artist.BLOOD_TYPE_OTHER

            birth_date = get_valid_date(birth_date)

            artist, created = self.update_or_create(
                melon_id=artist_id,
                defaults={
                    'name': name,
                    'real_name': real_name,
                    'nationality': nationality,
                    'birth_date': birth_date,
                    'constellation': constellation,
                    'blood_type': blood_type,
                    'intro': intro,
                }
            )

            temp_file = download(url_img_cover)
            file_name = '{artist_id}.{ext}'.format(
                artist_id=artist_id,
                ext=get_buffer_ext(temp_file)
            )
            if artist.img_profile:
                artist.img_profile.delete()
            artist.img_profile.save(file_name, File(temp_file))

            return artist, created
