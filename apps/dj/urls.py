from django.urls import path
from . import views

app_name = "dj"

urlpatterns = [
    # path("dj/beatport", views.beatport_techno_top100_scraper, name="beatport"),
    # API
    path("api/dj/beatport", views.beatport_techno_top100_scraper, name="api_beatport"),
]
