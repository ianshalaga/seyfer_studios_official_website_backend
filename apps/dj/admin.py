from django.contrib import admin
from . import models

# Register your models here.


# @admin.register(models.Song)
# class SongAdmin(admin.ModelAdmin):
#     list_display = ["name", "state"]
#     search_fields = ["name", "state", "artists__name"]
#     list_filter = ["state", "artists__name"]
#     ordering = ["name"]


# @admin.register(models.Artist)
# class ArtistAdmin(admin.ModelAdmin):
#     list_display = ["name", "state"]
#     search_fields = ["name", "state", "songs__name"]
#     list_filter = ["state", "songs__name"]
#     ordering = ["name"]
