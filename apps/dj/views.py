# Python standar
from collections import defaultdict
# Django
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from .models import Artist, SongArtistStateEnum, Song
# External
from termcolor import cprint
# Own
from ..utilities.apps import dj
from ..utilities.apps.exceptions import *

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
        song_state = request.GET.get("state")
        songs: list = list()
        if not song_state:  # All songs
            songs = Song.objects.all().order_by("title")
        elif song_state == "YES":  # Allowed songs
            songs = Song.objects.filter(
                state=SongArtistStateEnum.YES).order_by("title")
        elif song_state == "BAN":  # Not allowed songs
            songs = Song.objects.filter(
                state=SongArtistStateEnum.BAN).order_by("title")
        elif song_state == "NEW":  # New songs
            songs = Song.objects.filter(
                state=SongArtistStateEnum.NEW).order_by("title")

        context = {
            "title": "Seyfer DJ Studio: Songs",
            "now": timezone.now(),
            "songs": songs,
        }
        return render(request, "dj/song_list.html", context)


class SongStateUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        song = get_object_or_404(Song, code=kwargs["code"])
        song.state = kwargs["new_state"]
        song.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))


class ArtistStateUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        artist = get_object_or_404(Artist, code=kwargs["code"])
        artist.state = kwargs["new_state"]
        artist.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))


# @@@@ API


def beatport_techno_top100_scraper(request):
    try:
        cprint(f"Beatport Techno Top 100 Scraping started", "blue")
        songs_list: list = dj.beatport_songs_artists_scraper(
            dj.BEATPORT_TECHNO_TOP100_URL)

        artists_ban: list[str] = dj.get_db_artists_banned()
        artists_yes: list[str] = dj.get_db_artists_allowed()

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

        songs_urls_set: set = set()
        songs_final_list: list = list()
        repeated_songs: int = 0

        for song in songs_list:
            if song["url"] not in songs_urls_set:
                songs_urls_set.add(song["url"])
                songs_final_list.append(song)
            else:
                repeated_songs += 1
                cprint(
                    f"Repeated song: {song['url']} | Total: {repeated_songs}", "yellow")

        for song in songs_final_list:
            artists_db_list: list = list()
            for artist in song["artists"]:
                if artist["name"] in artists_ban:
                    artist_db, _ = Artist.objects.update_or_create(
                        name=artist["name"],
                        link=artist["url"],
                        state=SongArtistStateEnum.BAN,
                    )
                elif artist["name"] in artists_yes:
                    artist_db, _ = Artist.objects.update_or_create(
                        name=artist["name"],
                        link=artist["url"],
                        state=SongArtistStateEnum.YES,
                    )
                else:
                    artist_db, _ = Artist.objects.update_or_create(
                        name=artist["name"],
                        link=artist["url"],
                        state=SongArtistStateEnum.NEW,
                    )

                artists_db_list.append(artist_db)

            song_db, _ = Song.objects.update_or_create(
                title=song["name"],
                link=song["url"],
                defaults={"state": SongArtistStateEnum.NEW},
            )

            song_db.artists.set(artists_db_list)
            song_db.save()

        return JsonResponse({"status": "success"})  # safe=False
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
