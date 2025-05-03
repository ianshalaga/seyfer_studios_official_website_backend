# My Modules
import django_initializer
# Standar Modules
import os
import sys
# Django Models
from apps.dj.models import Artist, Song, SongArtistStateEnum
# Mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

MUSIC_MP3_PATH: str = "F:/DESCARGAS/Música/@Ready/Melodic House & Techno"
MUSIC_MP3_FOLDER: str = os.path.abspath(MUSIC_MP3_PATH)

EASY_ID3_TAG_TITLE: str = "title"
EASY_ID3_TAG_ARTIST: str = "artist"


def mp3_load_metadata_into_db() -> None:
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
        print(f"{mp3_load_metadata_into_db.__name__}: {e}")


def get_artists_by_song(song_title: str) -> None:
    song = Song.objects.get(title=song_title)
    artists = song.artists.all()
    print(
        f"Artistas de {song_title}: {', '.join([artist.name for artist in artists])}")


# get_artists_by_song("Escape (John Summit Remix) [Extended Mix]")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(
            f"Usage: python {sys.argv[0]} [options]")
    if "-mp3-load" in sys.argv:
        mp3_load_metadata_into_db()
