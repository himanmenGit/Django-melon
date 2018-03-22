from django.urls import path

from ..apis import AuthTokenView, MyUserDetail, AuthTokenForFacebookAccessTokenView

urlpatterns = [
    path('auth-token/', AuthTokenView.as_view()),
    path('info/', MyUserDetail.as_view()),
    path('facebook-auth-token/', AuthTokenForFacebookAccessTokenView.as_view()),
]
