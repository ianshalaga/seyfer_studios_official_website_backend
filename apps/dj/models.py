from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class SongArtistStateEnum(models.TextChoices):
    YES = "YES", _("Allowed")
    NO = "NO", _("Not Allowed")
    NEW = "NEW", _("New")


STATE_MAX_LENGTH = max(len(choice.value) for choice in SongArtistStateEnum)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(
        max_length=STATE_MAX_LENGTH, choices=SongArtistStateEnum.choices)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100)
    state = models.CharField(
        max_length=STATE_MAX_LENGTH, choices=SongArtistStateEnum.choices)
    artists = models.ManyToManyField(Artist, related_name="songs")

    def __str__(self):
        return self.title
