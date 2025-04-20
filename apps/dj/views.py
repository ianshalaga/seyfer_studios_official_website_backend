from django.shortcuts import render
from .models import Artist, SongArtistStateEnum

# Create your views here.

BEATPORT_TECHNO_TOP100_URL = "https://www.beatport.com/genre/melodic-house-techno/90/top-100"


def beatport_techno_top100_scraper(request):
    # Esta función tiene que scrapear las canciones del top 100 de beatport.
    # Debe dar los enlaces a las canciones.
    # Si la canción se encuentra Allowed o Not Allowed en la base de datos, no debe mostrarse.
    # Si todos los artistas de una canción están baneados, la cancion debe ser baneada.
    # Si alguno de los artistas de una cancion no esta baneado, la cancion debe ser permitida.
    # Para cada artista Allowed y no registrado en la base de datos, se debe acceder a su top 10 personal.
    # De ese top 10 se deben obtener las canciones no registradas en la base de datos.

    return render(request, "dj/beatport.html", {})
