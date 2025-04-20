from django_initializer import DjangoInitializer
from apps.dj.models import Artist, Song, SongArtistStateEnum


for artist in Artist.objects.all():
    print(artist.name)
