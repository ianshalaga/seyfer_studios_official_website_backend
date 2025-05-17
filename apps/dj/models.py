from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class SongArtistStateEnum(models.TextChoices):
    YES = "YES", _("Allowed")
    BAN = "BAN", _("Not Allowed")
    NEW = "NEW", _("Pending")


STATE_MAX_LENGTH = max(len(choice.value) for choice in SongArtistStateEnum)


class Artist(models.Model):
    code = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    state = models.CharField(
        max_length=STATE_MAX_LENGTH, choices=SongArtistStateEnum.choices)

    def __str__(self):
        return self.name


class Song(models.Model):
    code = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    state = models.CharField(
        max_length=STATE_MAX_LENGTH, choices=SongArtistStateEnum.choices)
    artists = models.ManyToManyField(Artist, related_name="songs")

    def __str__(self):
        return f"{self.title} by {', '.join([artist.name for artist in self.artists.all()])}"
