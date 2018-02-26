import datetime

from django import forms

from .models import Album

__all__ = (
    'AlbumForm',
)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album

        fields = '__all__'
        exclude = ['album_id', 'like_users']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '제목'}
            ),
            'release_date': forms.SelectDateWidget(
                years=range(datetime.date.today().year - 100, datetime.date.today().year + 1),
                attrs={'class': 'form-control'}
            ),
        }
