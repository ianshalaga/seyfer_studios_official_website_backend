from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["title", "state"]
    search_fields = ["title", "state", "artists__name"]
    list_filter = ["state", "artists__name"]
    ordering = ["title"]


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name", "state"]
    search_fields = ["name", "state", "songs__title"]
    list_filter = ["state", "songs__title"]
    ordering = ["name"]
