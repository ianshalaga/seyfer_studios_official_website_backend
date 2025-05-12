# from django.shortcuts import render
from django.http import JsonResponse
from .models import Artist, SongArtistStateEnum
from bs4 import BeautifulSoup
from ..utilities.scripts.dj import selenium_request


# Create your views here.

# with open("apps/dj/test.html", "r", encoding="utf-8") as f:
#     HTML = f.read()

BEATPORT_URL_BASE = "https://www.beatport.com"
BEATPORT_TECHNO_TOP100_URL = BEATPORT_URL_BASE + \
    "/genre/melodic-house-techno/90/top-100"


def beatport_techno_top100_scraper(request):
    html = selenium_request(BEATPORT_TECHNO_TOP100_URL)

    soup = BeautifulSoup(html, "html.parser")
    songs_blocks = soup.select("div.Lists-shared-style__MetaRow-sc-d366b33c-4")
    song_links_list = list()
    for song_block in songs_blocks:
        song_link = BEATPORT_URL_BASE + song_block.select_one("a").get("href")
        song_links_list.append(song_link)
        print(song_link)
        song_tag = song_block.select_one(
            "span.Lists-shared-style__ItemName-sc-d366b33c-7")
        song_name_and_extra = list(song_tag.stripped_strings)
        artists_block = song_block.select_one("div.ArtistNames-sc-72fc6023-0")
        artist = list()
        for a in artists_block.select("a"):
            artist.append({a.get("title"): BEATPORT_URL_BASE + a.get("href")})

    context = {"context": soup}
    # return render(request, "dj/base.html", context)
    return JsonResponse(song_links_list, safe=False)

    # Esta función tiene que scrapear las canciones del top 100 de beatport.
    # Debe dar los enlaces a las canciones.
    # Si la canción se encuentra Allowed o Not Allowed en la base de datos, no debe mostrarse.
    # Si todos los artistas de una canción están baneados, la cancion debe ser baneada.
    # Si alguno de los artistas de una cancion no esta baneado, la cancion debe ser permitida.
    # Para cada artista Allowed y no registrado en la base de datos, se debe acceder a su top 10 personal.
    # De ese top 10 se deben obtener las canciones no registradas en la base de datos.
