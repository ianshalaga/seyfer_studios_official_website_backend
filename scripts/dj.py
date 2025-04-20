import django_initializer
import os
from apps.dj.models import Artist, Song, SongArtistStateEnum
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

MUSIC_MP3_PATH = os.path.abspath(
    "F:/DESCARGAS/Música/@Ready/Melodic House & Techno")


def mp3_load_metadata_into_db():
    for mp3_file in os.listdir(MUSIC_MP3_PATH):
        if not mp3_file.endswith(".mp3"):
            continue

        mp3_path = os.path.join(MUSIC_MP3_PATH, mp3_file)
        mp3_audio = MP3(mp3_path, ID3=EasyID3)

        mp3_title = mp3_audio.get("title", [""])[0]  # Song title
        mp3_artists = mp3_audio.get("artist", [""])[
            0].split(", ")  # Artists list

        artists = list()
        for artist_name in mp3_artists:
            artist, _ = Artist.objects.get_or_create(
                name=artist_name, defaults={"state": SongArtistStateEnum.NEW})
            artists.append(artist)

        mp3_song, _ = Song.objects.get_or_create(
            title=mp3_title, defaults={"state": SongArtistStateEnum.YES})

        mp3_song.artists.add(*artists)

        print(f"✔ Cargado: {mp3_title} por {", ".join(mp3_artists)}")


def get_artists_by_song(song_title: str):
    song = Song.objects.get(title=song_title)
    artists = song.artists.all()
    print(
        f"Artistas de {song_title}: {', '.join([artist.name for artist in artists])}")


# mp3_load_metadata_into_db()
# get_artists_by_song("Escape (John Summit Remix) [Extended Mix]")
