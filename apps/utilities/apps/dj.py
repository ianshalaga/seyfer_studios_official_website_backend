# Standar Modules
import os
import time
# Django Models
from ...dj.models import Artist, Song, SongArtistStateEnum
# Mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
# Selenium
from selenium import webdriver
# Termcolor
from termcolor import cprint
# BeautifulSoup
from bs4 import BeautifulSoup

# Music
MUSIC_MP3_PATH: str = "F:/DESCARGAS/Música/@Ready/Melodic House & Techno"
MUSIC_MP3_FOLDER: str = os.path.abspath(MUSIC_MP3_PATH)

# Easy ID3 Tags
EASY_ID3_TAG_TITLE: str = "title"
EASY_ID3_TAG_ARTIST: str = "artist"

# Beatport URLs
BEATPORT_URL_BASE = "https://www.beatport.com"
BEATPORT_TECHNO_TOP100_URL = "".join(
    [BEATPORT_URL_BASE, "/genre/melodic-house-techno/90/top-100"])

# Artists files
ARTISTS_YES_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_yes.txt"))
ARTISTS_BAN_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_ban.txt"))


class BeatportSong():
    def __init__(self, title: str, variation: str, url: str, artists: list[dict] = []):
        self.__title: str = title
        self.__variation: str = variation
        self.__url: str = url
        self.__artists = artists

    def name(self) -> str:
        try:
            name: str = ""
            if "(" in self.__title and ")" in self.__title:
                name = " ".join([self.__title, f"[{self.__variation}]"])
            else:
                name = " ".join([self.__title, f"({self.__variation})"])
            return name
        except Exception as e:
            print(
                f"{__class__} | {__name__} | Ocurrió un error inesperado: {repr(e)}")

    def get_url(self):
        return self.__url

    def set_artists(self, artists: list[dict]):
        self.__artists = artists

    def serialize(self):
        return {
            "name": self.name(),
            "url": self.__url,
            "artists": self.__artists
        }


class BeatportArtist():
    def __init__(self, name: str, url: str):
        self.__name: str = name
        self.__url: str = url

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def serialize(self):
        return {
            "name": self.__name,
            "url": self.__url,
        }


def mp3_load_metadata_into_db() -> None:  # @@@@
    try:
        for file in os.listdir(MUSIC_MP3_FOLDER):
            if not file.endswith(".mp3"):
                continue

            mp3_file: str = file

            mp3_path: str = os.path.join(MUSIC_MP3_FOLDER, mp3_file)
            mp3_audio: MP3 = MP3(mp3_path, ID3=EasyID3)

            mp3_title: str = mp3_audio.get(EASY_ID3_TAG_TITLE, [""])[
                0]  # Song title
            mp3_artists: list[str] = mp3_audio.get(EASY_ID3_TAG_ARTIST, [""])[
                0].split(", ")  # Artists list

            artists: list[Artist] = list()
            for artist_name in mp3_artists:
                artist, _ = Artist.objects.get_or_create(
                    name=artist_name, defaults={"state": SongArtistStateEnum.NEW})
                artists.append(artist)

            mp3_song, created = Song.objects.get_or_create(
                title=mp3_title, defaults={"state": SongArtistStateEnum.YES})

            mp3_song.artists.add(*artists)

            if created:
                print(f"✅ Added: {mp3_title} by {", ".join(mp3_artists)}")
            else:
                print(f"⚠ Existing: {mp3_title} by {", ".join(mp3_artists)}")
    except Exception as e:
        # print(f"{__name__}: {e}")
        print(f"{mp3_load_metadata_into_db.__name__}: {e}")


def get_artists_by_song(song_title: str) -> None:
    song = Song.objects.get(title=song_title)
    artists = song.artists.all()
    print(
        f"Artistas de {song_title}: {', '.join([artist.name for artist in artists])}")


def request_dynamic(url: str, delay: int = 5) -> str:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        time.sleep(delay)  # Waiting for JS to load
        html = browser.page_source
        browser.quit()
        return html
    except Exception as e:
        print(f"{__name__} | Ocurrió un error inesperado: {repr(e)}")


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

        cprint(f"✅ Songs allowed: {songs_allowed}", "green")
        cprint(f"❌ Songs not allowed: {songs_not_allowed}", "red")
        cprint(f"🎶 Songs total: {songs_allowed + songs_not_allowed}", "blue")

        return songs_list
    except Exception as e:
        print(f"{__name__} | Error: {repr(e)}")


def get_db_artists_banned():
    try:
        artists_ban: list[str] = [artist_db.name for artist_db in Artist.objects.filter(
            state=SongArtistStateEnum.BAN)]  # Get database artists banned
        return artists_ban
    except Exception as e:
        cprint(f"{__name__} | Error: {repr(e)}", "red")


def get_db_songs_allowed():
    try:
        songs_yes: list[str] = [song_db.title for song_db in Song.objects.filter(
            state=SongArtistStateEnum.YES)]  # Get database songs allowed
        return songs_yes
    except Exception as e:
        cprint(f"{__name__} | Error: {repr(e)}", "red")


def get_db_songs_not_allowed():
    try:
        songs_ban: list[str] = [song_db.title for song_db in Song.objects.filter(
            state=SongArtistStateEnum.BAN)]  # Get database songs allowed
        return songs_ban
    except Exception as e:
        cprint(f"{__name__} | Error: {repr(e)}", "red")
