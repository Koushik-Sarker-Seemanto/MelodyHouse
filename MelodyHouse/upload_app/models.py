from django.db import models
from django.contrib.auth.models import Permission
from authentication.models import Account

# Create your models here.

_GENRES = (
    ('Rock', 'Rock'),
    ('Metal', 'Metal'),
    ('Romantic', 'Romantic'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Jazz', 'Jazz'),
    ('Folk', 'Folk'),
    ('Rap', "Rap"),
)


class Album(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=50, choices=_GENRES)
    description = models.CharField(max_length=1000, default='', blank=True)

    class Meta:
        unique_together = (('album_title', 'artist', 'user'),)

    def __str__(self):
        return self.album_title + ' - ' + self.artist
