from django.urls import path
from . import views

app_name = "dj"

urlpatterns = [
    path("dj/load-artists", views.load_artists)
]
