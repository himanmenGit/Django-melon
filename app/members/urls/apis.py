from django.urls import path

from ..apis import AuthTokenView, MyUserDetail

urlpatterns = [
    path('auth-token/', AuthTokenView.as_view()),
    path('info/', MyUserDetail.as_view()),
]
