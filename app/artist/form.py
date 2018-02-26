import datetime
from django import forms

from .models import Artist

__all__ = (
    'ArtistForm',
)


# ModelForm을 사용하여 Form을 만들면
# Model에 있는 기능을 사용할 수 있다.
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'
        exclude = ['melon_id', 'like_users']
        widgets = {
            # 'img_profile': forms.FileInput(
            #     attrs={'class': 'form-control'}
            # ),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '이름'}
            ),
            'real_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '본명'}
            ),
            'nationality': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '국적'}
            ),

            'birth_date': forms.SelectDateWidget(
                years=range(datetime.date.today().year - 100, datetime.date.today().year + 1),
                attrs={'class': 'form-control'}
            ),
            'constellation': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '별자리'}
            ),
            'blood_type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'intro': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '소개'}
            ),
        }
