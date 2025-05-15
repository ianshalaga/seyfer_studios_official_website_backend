from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import render
from .models import Artist, SongArtistStateEnum, Song
from termcolor import cprint
from ..utilities.apps import dj
from ..utilities.apps.exceptions import *
from django.views import View
from django.utils import timezone


# Create your views here.


# @@@@ TEMPLATES


class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Seyfer DJ Studio",
            "now": timezone.now(),
        }
        return render(request, "dj/index.html", context)


class SongListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # songs = Song.objects.filter(
        #     state=SongArtistStateEnum.BAN).order_by("title")
        songs = Song.objects.all().order_by("title")
        context = {
            "title": "Seyfer DJ Studio: Songs",
            "now": timezone.now(),
            "songs": songs,
        }
        return render(request, "dj/song_list.html", context)


# @@@@ API


def beatport_techno_top100_scraper(request):
    try:
        cprint(f"Beatport Techno Top 100 Scraping started", "blue")
        songs_list: list = dj.beatport_songs_artists_scraper(
            dj.BEATPORT_TECHNO_TOP100_URL)

        artists_ban: list[str] = dj.get_db_artists_banned()

        artists_url_set: set = set()

        for song in songs_list:
            for artist in song["artists"]:
                if artist["name"] not in artists_ban:
                    artists_url_set.add(artist["url"])

        artists_url_list = list(artists_url_set)

        songs_list_by_artist: list = list()

        for i, artist_url in enumerate(artists_url_list):
            cprint(
                f"Scraping started | {i+1}/{len(artists_url_list)} | {artist_url}", "yellow")
            songs_list_by_artist.extend(
                dj.beatport_songs_artists_scraper(artist_url))

        songs_list.extend(songs_list_by_artist)

        artists_names_set: set[str] = {
            artist["name"]
            for song in songs_list
            for artist in song["artists"]
            if artist["name"] not in artists_ban
        }

        artists_names_list: list[str] = list(artists_names_set)

        response_dict_sets: dict = defaultdict(set)
        for artist in artists_names_list:
            for song in songs_list:
                if artist in [art["name"] for art in song["artists"]]:
                    response_dict_sets[artist].add(song["url"])

        response_dict_lists: dict = dict(sorted({artist: sorted(
            songs) for artist, songs in response_dict_sets.items()}.items()))

        return JsonResponse(response_dict_lists)  # safe=False
    except (DynamicRequestError, ScraperError, DatabaseAccessError) as e:
        error: str = f"{__name__} | {beatport_techno_top100_scraper.__name__} | {e}"
        cprint(error, "red")
        return JsonResponse({"error": error})
    except Exception as e:
        error: str = f"{__name__} | {beatport_techno_top100_scraper.__name__} | {e}"
        cprint(error, "red")
        return JsonResponse({"error": error})


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
