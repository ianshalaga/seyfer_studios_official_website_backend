import os
from collections import defaultdict
from django.http import JsonResponse
from .models import Artist, SongArtistStateEnum
from termcolor import cprint
from ..utilities.apps import dj


# Create your views here.


def beatport_techno_top100_scraper(request):
    # try:
    cprint(f"Beatport Techno Top 100 Scraping started", "blue")
    songs_list: list = dj.beatport_songs_artists_scraper(
        dj.BEATPORT_TECHNO_TOP100_URL)

    cprint(songs_list, "cyan")

    artists_ban: list[str] = dj.get_db_artists_banned()

    artists_url_set: set = set()
    for song in songs_list:
        for artist in song["artists"]:
            if artist["name"] not in artists_ban:
                artists_url_set.add(artist["url"])
    artists_url_list = list(artists_url_set)

    songs_list_by_artist: list = list()

    for i, artist_url in enumerate(artists_url_list[:1]):
        cprint(
            f"Scraping started | {i+1}/{len(artists_url_list)} | {artist_url}", "yellow")
        songs_list_by_artist.extend(
            dj.beatport_songs_artists_scraper(artist_url))

    cprint(songs_list_by_artist, "magenta")

    # @@@@
    # Obtener todos los artistas sin repetición desde song_list y desde song_list_by_artist
    songs_list.extend(songs_list_by_artist)
    cprint(songs_list, "cyan")
    artists_names_set: set[str] = {artist["name"]
                                   for song in songs_list for artist in song["artists"]}
    artists_names_list: list[str] = list(artists_names_set)

    response_dict_sets: dict = defaultdict(set)
    for artist in artists_names_list:
        for song in songs_list:
            if artist in [art["name"] for art in song["artists"]]:
                response_dict_sets[artist].add(song["url"])

    response_dict_lists: dict = dict(sorted({artist: sorted(
        songs) for artist, songs in response_dict_sets.items()}.items()))
    # @@@@

    # songs_definitive_set: set[str] = {song["url"]
    #                                   for song in songs_list_by_artist}

    # songs_definitive_set.update({song["url"] for song in songs_list})
    # songs_definitive_list: list[str] = list(songs_definitive_set)

    # return JsonResponse(songs_definitive_list, safe=False)
    return JsonResponse(response_dict_lists)
    # except Exception as e:
    #     cprint(
    #         f"File: {__name__} | {beatport_techno_top100_scraper.__name__} | Error: {repr(e)}")
    #     return JsonResponse({"Error": f"{e}"})


def load_yes_artists_into_db(request):
    try:
        with open(dj.ARTISTS_YES_FILE_PATH, "r", encoding="utf-8") as file:
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
        with open(dj.ARTISTS_BAN_FILE_PATH, "r", encoding="utf-8") as file:
            data = [line.strip() for line in file.readlines()]
            for artist in data:
                artist_db, _ = Artist.objects.get_or_create(name=artist)
                artist_db.state = SongArtistStateEnum.BAN
                artist_db.save()
        return JsonResponse({"state": "success"}, status=200)
    except Exception as e:
        print(f"{__name__} | Exception: {repr(e)}")
        return JsonResponse({"state": "error", "error": str(e)}, status=500)
