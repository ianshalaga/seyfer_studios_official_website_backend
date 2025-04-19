
import django_init
from dj.models import Artist, SongArtistStateEnum


for artist in Artist.objects.all():
    print(artist.name)
