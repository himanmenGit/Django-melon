from django.urls import path

from ..apis import AuthTokenView

app_name = 'members'
urlpatterns = [
    path('auth-token/', AuthTokenView.as_view(), name='auth-token'),
]
