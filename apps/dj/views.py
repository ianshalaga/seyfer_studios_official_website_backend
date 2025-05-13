# from django.shortcuts import render
from django.http import JsonResponse
from .models import Song, Artist, SongArtistStateEnum
from bs4 import BeautifulSoup
from ..utilities.apps.dj import request_dynamic, BeatportSong, BeatportArtist
import os


# Create your views here.

# Beatport URLs
BEATPORT_URL_BASE = "https://www.beatport.com"
BEATPORT_TECHNO_TOP100_URL = "".join(
    [BEATPORT_URL_BASE, "/genre/melodic-house-techno/90/top-100"])

# Artists files
ARTISTS_YES_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_yes.txt"))
ARTISTS_BAN_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_ban.txt"))


def get_db_artists_banned():
    artists_ban: list[str] = [artist_db.name for artist_db in Artist.objects.filter(
        state=SongArtistStateEnum.BAN)]  # Get database artists banned
    return artists_ban


def get_db_songs_allowed():
    songs_yes: list[str] = [song_db.title for song_db in Song.objects.filter(
        state=SongArtistStateEnum.YES)]  # Get database songs allowed
    return songs_yes


def get_db_songs_not_allowed():
    songs_ban: list[str] = [song_db.title for song_db in Song.objects.filter(
        state=SongArtistStateEnum.BAN)]  # Get database songs allowed
    return songs_ban


def beatport_techno_top100_scraper(request):
    print(f"Beatport Techno Top 100 songs | Scraping started")
    songs_list: list = beatport_songs_artists_scraper(
        BEATPORT_TECHNO_TOP100_URL)
    print(f"Beatport Techno Top 100 songs | Scraping finished")

    artists_ban: list[str] = get_db_artists_banned()

    artists_url_set: set = set()
    for song in songs_list:
        for artist in song["artists"]:
            if artist["name"] not in artists_ban:
                artists_url_set.add(artist["url"])
    artists_url_list = list(artists_url_set)

    songs_list_by_artist: list = list()

    for i, artist_url in enumerate(artists_url_list):
        print(
            f"Scraping started | {i+1}/{len(artists_url_list)} | {artist_url}")
        songs_list_by_artist.extend(beatport_songs_artists_scraper(artist_url))
        print(
            f"Scraping finished | {i+1}/{len(artists_url_list)} | {artist_url}")

    songs_definitive_set: set[str] = {song["url"]
                                      for song in songs_list_by_artist}

    songs_definitive_set.update({song["url"] for song in songs_list})
    songs_definitive_list: list[str] = list(songs_definitive_set)

    return JsonResponse(songs_definitive_list, safe=False)

    # Esta función tiene que scrapear las canciones del top 100 de beatport.
    # Debe dar los enlaces a las canciones.
    # Si la canción se encuentra Allowed o Not Allowed en la base de datos, no debe mostrarse.
    # Si todos los artistas de una canción están baneados, la cancion debe ser baneada.
    # Si alguno de los artistas de una cancion no esta baneado, la cancion debe ser permitida.
    # Para cada artista Allowed y no registrado en la base de datos, se debe acceder a su top 10 personal.
    # De ese top 10 se deben obtener las canciones no registradas en la base de datos.


def beatport_songs_artists_scraper(beatport_url: str):
    try:
        artists_ban: list[str] = get_db_artists_banned()
        songs_yes: list[str] = get_db_songs_allowed()
        songs_ban: list[str] = get_db_songs_not_allowed()

        songs_allowed: int = 0
        songs_not_allowed: int = 0

        # Get dynamic HTML from beatport_url
        html: str = request_dynamic(beatport_url)
        soup = BeautifulSoup(
            html, "html.parser")  # Parse HTML with bs4

        songs_html_blocks = soup.select(
            "div.Lists-shared-style__MetaRow-sc-d366b33c-4")  # Get all songs html blocks
        songs_list: list[dict] = list()

        for song_html_block in songs_html_blocks:  # For each song html block
            artists_html_block = song_html_block.select_one(
                "div.ArtistNames-sc-72fc6023-0")  # Get artists html block

            artists_list: list[dict] = list()
            allowed_song: bool = False

            # For each artist html a tag in block
            for artist_html_tag_a in artists_html_block.select("a"):
                artist_name: str = artist_html_tag_a.get(
                    "title")  # Get artist name
                if artist_name not in artists_ban:  # One allowed artist is enough to allowed the song
                    allowed_song = True
                artist_url: str = "".join(
                    [BEATPORT_URL_BASE, artist_html_tag_a.get("href")])
                beatport_artist = BeatportArtist(
                    artist_name, artist_url)  # Create beatport artist instance
                artists_list.append(beatport_artist.serialize())

            if not allowed_song:  # All artist must be YES to allow the song
                songs_not_allowed += 1
                continue

            song_url = "".join(
                [BEATPORT_URL_BASE, song_html_block.select_one("a").get("href")])
            song_html_tag_span = song_html_block.select_one(
                "span.Lists-shared-style__ItemName-sc-d366b33c-7")
            song_title_variation: list[str] = list(
                song_html_tag_span.stripped_strings)
            song_title: str = song_title_variation[0]
            song_variation: str = song_title_variation[1]
            beatport_song = BeatportSong(song_title, song_variation, song_url)

            if beatport_song.name() in songs_yes or beatport_song.name() in songs_ban:
                songs_not_allowed += 1
                continue

            beatport_song.set_artists(artists_list)
            songs_list.append(beatport_song.serialize())
            songs_allowed += 1

        print(f"Songs allowed: {songs_allowed}")
        print(f"Songs not allowed: {songs_not_allowed}")
        print(f"Songs total: {songs_allowed + songs_not_allowed}")

        return songs_list
    except Exception as e:
        print(f"{__name__} | Error: {repr(e)}")


def load_yes_artists_into_db(request):
    try:
        with open(ARTISTS_YES_FILE_PATH, "r", encoding="utf-8") as file:
            data = [line.strip() for line in file.readlines()]
            for artist in data:
                artist_db, _ = Artist.objects.get_or_create(name=artist)
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
                artist_db, _ = Artist.objects.get_or_create(name=artist)
                artist_db.state = SongArtistStateEnum.BAN
                artist_db.save()
        return JsonResponse({"state": "success"}, status=200)
    except Exception as e:
        print(f"{__name__} | Exception: {repr(e)}")
        return JsonResponse({"state": "error", "error": str(e)}, status=500)
