from django.urls import path
from . import views

app_name = "dj"

urlpatterns = [
    # TEMPLATES
    path("", views.IndexView.as_view(), name="index"),
    path("song/list", views.SongListView.as_view(), name="song_list"),
    #
    path("song/<uuid:code>/state/<str:new_state>",
         views.SongStateUpdateView.as_view(), name="song_state_update"),
    path("artist/<uuid:code>/state/<str:new_state>",
         views.ArtistStateUpdateView.as_view(), name="artist_state_update"),
    # API
    path("api/beatport", views.beatport_techno_top100_scraper, name="api_beatport"),
    path("api/beatport/artists/yes", views.load_yes_artists_into_db,
         name="api_beatport_artists_yes"),
    path("api/beatport/artists/ban", views.load_ban_artists_into_db,
         name="api_beatport_artists_ban"),
]
