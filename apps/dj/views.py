# from django.shortcuts import render
from django.http import JsonResponse
from .models import Song, Artist, SongArtistStateEnum
from bs4 import BeautifulSoup
from ..utilities.apps.dj import request_dynamic, BeatportSong, BeatportArtist
import os


# Create your views here.

# with open("apps/dj/test.html", "r", encoding="utf-8") as f:
#     HTML = f.read()

BEATPORT_URL_BASE = "https://www.beatport.com"
BEATPORT_TECHNO_TOP100_URL = "".join(
    [BEATPORT_URL_BASE, "/genre/melodic-house-techno/90/top-100"])

ARTISTS_YES_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_yes.txt"))
ARTISTS_BAN_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_ban.txt"))


def beatport_techno_top100_scraper(request):
    html: str = request_dynamic(BEATPORT_TECHNO_TOP100_URL)

    soup = BeautifulSoup(html, "html.parser")

    artists_ban = [artist_db.name for artist_db in Artist.objects.filter(
        state=SongArtistStateEnum.BAN)]
    songs_yes = [song_db.title for song_db in Song.objects.filter(
        state=SongArtistStateEnum.YES)]

    songs_filtered = 0
    songs_pass = 0

    songs_blocks = soup.select("div.Lists-shared-style__MetaRow-sc-d366b33c-4")
    songs_list: list = list()
    for song_block in songs_blocks:
        # Artists
        artists_block = song_block.select_one("div.ArtistNames-sc-72fc6023-0")
        artists_list = list()
        valid_song = False
        for a_tag_artist in artists_block.select("a"):
            artist_name = a_tag_artist.get("title")
            if artist_name not in artists_ban:
                valid_song = True
            artist_url = "".join([BEATPORT_URL_BASE, a_tag_artist.get("href")])
            beatport_artist = BeatportArtist(
                artist_name, artist_url)
            artists_list.append(beatport_artist.serialize())
        if not valid_song:
            songs_filtered += 1
            continue
        # Songs
        song_url = BEATPORT_URL_BASE + song_block.select_one("a").get("href")
        song_tag = song_block.select_one(
            "span.Lists-shared-style__ItemName-sc-d366b33c-7")
        song_title_variation = list(song_tag.stripped_strings)
        song_title = song_title_variation[0]
        song_variation = song_title_variation[1]
        beatport_song = BeatportSong(song_title, song_variation, song_url)
        if beatport_song.name() in songs_yes:
            songs_filtered += 1
            continue
        #
        beatport_song.set_artists(artists_list)
        songs_list.append(beatport_song.serialize())
        songs_pass += 1

    print(songs_pass, songs_filtered, songs_pass + songs_filtered)

    # context = {"context": soup}
    # return render(request, "dj/base.html", context)
    return JsonResponse(songs_list, safe=False)

    # Esta función tiene que scrapear las canciones del top 100 de beatport.
    # Debe dar los enlaces a las canciones.
    # Si la canción se encuentra Allowed o Not Allowed en la base de datos, no debe mostrarse.
    # Si todos los artistas de una canción están baneados, la cancion debe ser baneada.
    # Si alguno de los artistas de una cancion no esta baneado, la cancion debe ser permitida.
    # Para cada artista Allowed y no registrado en la base de datos, se debe acceder a su top 10 personal.
    # De ese top 10 se deben obtener las canciones no registradas en la base de datos.


def load_yes_artists_into_db(request):
    try:
        with open(ARTISTS_YES_FILE_PATH, "r", encoding="utf-8") as file:
            data = [line.strip() for line in file.readlines()]
            for artist in data:
                artist_db, created = Artist.objects.get_or_create(name=artist)
                artist_db.state = SongArtistStateEnum.YES
                artist_db.save()
        return JsonResponse({"state": "success"}, status=200)
    except Exception as e:
        print(f"{__name__} | Exception: {repr(e)}")
        return JsonResponse({"state": "error", "error": str(e)}, status=500)


def load_ban_artists_into_db(request):
    try:
        with open(ARTISTS_BAN_FILE_PATH, "r", encoding="utf-8") as file:
            data = [line.strip() for line in file.readlines()]
            for artist in data:
                artist_db, created = Artist.objects.get_or_create(name=artist)
                artist_db.state = SongArtistStateEnum.BAN
                artist_db.save()
        return JsonResponse({"state": "success"}, status=200)
    except Exception as e:
        print(f"{__name__} | Exception: {repr(e)}")
        return JsonResponse({"state": "error", "error": str(e)}, status=500)
