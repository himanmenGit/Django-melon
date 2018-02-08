from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.artist_list, name='artist-list'),
]
