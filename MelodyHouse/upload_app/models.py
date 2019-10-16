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
    artist = models.CharField(max_length=100)
    album_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=_GENRES)
    description = models.TextField(max_length=1000, default='', blank=True)

    class Meta:
        unique_together = (('album_title', 'artist', 'user'),)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    song_title = models.CharField(max_length=100)
    song_file = models.CharField(max_length=500)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, )
    description = models.TextField(max_length=1000, default='', blank=True)

    class Meta:
        unique_together = (('song_file', 'album_id'), )

    def __str__(self):
        return self.song_title

               # + Album.objects.filter(album_id=self.album_id)
