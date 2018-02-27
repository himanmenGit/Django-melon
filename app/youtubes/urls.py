from django.urls import path

from . import views

app_name = 'youtube'
urlpatterns = [
    path('add/', views.youtube_add, name='youtube-add'),
]
