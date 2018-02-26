from django import forms

from artist.models import Artist

__all__ = (
    'ArtistAddForm',
)


# ModelForm을 사용하여 Form을 만들면
# Model에 있는 기능을 사용할 수 있다.
class ArtistAddForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'
        exclude = ['melon_id']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            )
        }
        # fields = [
        #     'img_profile',
        #     'name',
        #     'real_name',
        #     'nationality',
        #     'birth_date',
        #     'constellation',
        #     'blood_type',
        #     'intro',
        # ]
    # melon_id = forms.CharField(label='아티스트 ID')
    # img_profile = forms.ImageField(label='프로필 이미지')
    # real_name = forms.CharField(label='이름', max_length=50)
    # name = forms.CharField(label='본명', max_length=50)
    # nationality = forms.CharField(label='국적', max_length=50)
    # birth_date = forms.DateField(label='생년월일')
    # constellation = forms.CharField(label='별자리', max_length=30)
    # blood_type = forms.CharField(label='혈액형', max_length=30)
    # intro = forms.CharField(label='소개', widget=forms.Textarea)
