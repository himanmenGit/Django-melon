from django import forms

from .models import Song

__all__ = (
    'SongForm',
)


class SongForm(forms.ModelForm):
    class Meta:
        model = Song

        fields = '__all__'
        exclude = ['melon_id', 'like_users']
        widgets = {
            'album': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'artists': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '제목'}
            ),
            'genre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '장르'}
            ),
            'lyrics': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '가사'}
            ),
        }
