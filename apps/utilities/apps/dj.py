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
from termcolor import cprint, colored
# BeautifulSoup
from bs4 import BeautifulSoup
# Custom exceptions
from .exceptions import *

# Music Local
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
    os.path.dirname(__file__), "files", "artists_yes.txt"))  # Artist yes
ARTISTS_BAN_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "files", "artists_ban.txt"))  # Artist ban


class ScrapHtml():
    def __init__(self, tag, css_class):
        self.__tag = tag
        self.__css_class = css_class

    def get_tag(self):
        return self.__tag

    def get_css_class(self):
        return self.__css_class

    def set_tag(self, tag):
        self.__tag = tag

    def set_css_class(self, css_class):
        self._css_class = css_class

    def serialize(self):
        return ".".join([self.__tag, self.__css_class])


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


def request_dynamic(url: str, delay: int = 5) -> str:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        time.sleep(delay)  # Waiting for JS to load
        html = browser.page_source
        if not html:
            raise DynamicRequestError(
                f"{__name__} | {request_dynamic.__name__} | {url} | {html}"
            )
        browser.quit()
        return html
    except DynamicRequestError:
        raise
    except Exception as e:
        raise e


def beatport_songs_artists_scraper(beatport_url: str):
    try:
        try:
            artists_ban: list[str] = get_db_artists_banned()
            songs_yes: list[str] = get_db_songs_allowed()
            songs_ban: list[str] = get_db_songs_not_allowed()
        except Exception as e:
            raise DatabaseAccessError(
                f"{__name__} | {beatport_songs_artists_scraper.__name__} | {e}"
            )

        scrap_html_songs_blocks = ScrapHtml(
            "div",
            "Lists-shared-style__MetaRow-sc-cd3f7e11-4"
        )
        scrap_html_artist_block = ScrapHtml(
            "div",
            "ArtistNames-sc-72fc6023-0"
        )
        scrap_html_tag_span = ScrapHtml(
            "span",
            "Lists-shared-style__ItemName-sc-cd3f7e11-7"
        )

        songs_allowed: int = 0
        songs_not_allowed: int = 0

        html: str = request_dynamic(beatport_url)

        if scrap_html_songs_blocks.get_css_class() not in html:
            raise ScraperError(
                f"{__name__} | {beatport_songs_artists_scraper.__name__} | Invalid HTML")

        soup = BeautifulSoup(
            html, "html.parser")  # Parse HTML with bs4

        if not soup:
            raise ScraperError(
                f"{__name__} | {beatport_songs_artists_scraper.__name__} | HTML parse failed")

        songs_html_blocks = soup.select(
            scrap_html_songs_blocks.serialize())  # Get all songs html blocks

        if not songs_html_blocks:
            raise ScraperError(
                f"{__name__} | {beatport_songs_artists_scraper.__name__} | No songs found")

        songs_list: list[dict] = list()

        for song_html_block in songs_html_blocks:  # For each song html block
            artists_html_block = song_html_block.select_one(
                scrap_html_artist_block.serialize())  # Get artists html block

            if not artists_html_block:
                raise ScraperError(
                    f"{__name__} | {beatport_songs_artists_scraper.__name__} | No artists found")

            artists_list: list[dict] = list()
            allowed_song: bool = False

            # For each artist html a tag in block
            for artist_html_tag_a in artists_html_block.select("a"):
                artist_name: str = artist_html_tag_a.get(
                    "title")  # Get artist name

                if not artist_name:
                    raise ScraperError(
                        f"{__name__} | {beatport_songs_artists_scraper.__name__} | No artist name found")

                if artist_name not in artists_ban:  # One allowed artist is enough to allowed the song
                    allowed_song = True

                artist_url: str = "".join(
                    [BEATPORT_URL_BASE, artist_html_tag_a.get("href")])

                if artist_url == BEATPORT_URL_BASE:
                    raise ScraperError(
                        f"{__name__} | {beatport_songs_artists_scraper.__name__} | No artist url found")

                beatport_artist = BeatportArtist(
                    artist_name, artist_url)  # Create beatport artist instance

                artists_list.append(beatport_artist.serialize())

            if not allowed_song:  # All artist must be YES to allow the song
                songs_not_allowed += 1
                continue

            song_url = "".join(
                [BEATPORT_URL_BASE, song_html_block.select_one("a").get("href")])

            if not song_url:
                raise ScraperError(
                    f"{__name__} | {beatport_songs_artists_scraper.__name__} | No song url found")

            song_html_tag_span = song_html_block.select_one(
                scrap_html_tag_span.serialize())

            if not song_html_tag_span:
                raise ScraperError(
                    f"{__name__} | {beatport_songs_artists_scraper.__name__} | No song title found")

            song_title_variation: tuple[str] = tuple(
                song_html_tag_span.stripped_strings)

            if len(song_title_variation) != 2:
                raise ScraperError(
                    f"{__name__} | {beatport_songs_artists_scraper.__name__} | Invalid song title variation")

            song_title: str = song_title_variation[0]
            song_variation: str = song_title_variation[1]
            beatport_song = BeatportSong(song_title, song_variation, song_url)

            if beatport_song.name() in songs_yes or beatport_song.name() in songs_ban:
                songs_not_allowed += 1
                continue

            beatport_song.set_artists(artists_list)
            songs_list.append(beatport_song.serialize())
            songs_allowed += 1

        cprint(f"🎶 Songs total: {songs_allowed + songs_not_allowed}", "blue")
        cprint(f"✅ Songs allowed: {songs_allowed}", "green")
        cprint(f"❌ Songs not allowed: {songs_not_allowed}", "red")

        return songs_list
    except ScraperError:
        raise
    except DatabaseAccessError:
        raise
    except DynamicRequestError:
        raise
    except Exception as e:
        raise e


def get_db_artists_banned():
    try:
        artists_ban: list[str] = [artist_db.name for artist_db in Artist.objects.filter(
            state=SongArtistStateEnum.BAN)]  # Get database artists banned
        return artists_ban
    except Exception as e:
        raise DatabaseAccessError(
            colored(
                f"{__name__} | {get_db_artists_banned.__name__} | {repr(e)}", "red")
        )


def get_db_songs_allowed():
    try:
        songs_yes: list[str] = [song_db.title for song_db in Song.objects.filter(
            state=SongArtistStateEnum.YES)]  # Get database songs allowed
        return songs_yes
    except Exception as e:
        raise DatabaseAccessError(
            colored(
                f"{__name__} | {get_db_artists_banned.__name__} | {repr(e)}", "red")
        )


def get_db_songs_not_allowed():
    try:
        songs_ban: list[str] = [song_db.title for song_db in Song.objects.filter(
            state=SongArtistStateEnum.BAN)]  # Get database songs allowed
        return songs_ban
    except Exception as e:
        raise DatabaseAccessError(
            colored(
                f"{__name__} | {get_db_artists_banned.__name__} | {repr(e)}", "red")
        )
