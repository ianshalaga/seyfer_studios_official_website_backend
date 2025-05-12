from django.urls import path
from . import views

app_name = "dj"

urlpatterns = [
    # path("dj/beatport", views.beatport_techno_top100_scraper, name="beatport"),
    # API
    path("api/dj/beatport", views.beatport_techno_top100_scraper, name="api_beatport"),
    path("api/dj/beatport/artists/yes", views.load_yes_artists_into_db,
         name="api_beatport_artists_yes"),
    path("api/dj/beatport/artists/ban", views.load_ban_artists_into_db,
         name="api_beatport_artists_ban"),
]
