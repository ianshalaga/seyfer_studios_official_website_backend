from django.shortcuts import render
from .models import Artist, SongArtistStateEnum

# Create your views here.


def load_artists(request):
    # for artist in artist_not_allowed:
    #     Artist.objects.get_or_create(
    #         name=artist, defaults={"state": SongArtistStateEnum.NO})
    ...
