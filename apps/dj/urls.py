from django.urls import path
from . import views

app_name = "dj"

urlpatterns = [
    # TEMPLATES
    path("", views.IndexView.as_view(), name="index"),
    path("song/list", views.SongListView.as_view(), name="song_list"),
    # API
    path("api/beatport", views.beatport_techno_top100_scraper, name="api_beatport"),
    path("api/beatport/artists/yes", views.load_yes_artists_into_db,
         name="api_beatport_artists_yes"),
    path("api/beatport/artists/ban", views.load_ban_artists_into_db,
         name="api_beatport_artists_ban"),
]
