from django.db import models
from django.contrib.auth.models import Permission
from authentication.models import Account
from upload_app.models import Song,Album
from datetime import datetime


class Post(models.Model):
    post_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    post_song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True,null=True)
    date_time = models.DateTimeField(default=datetime.now)
    post_type = models.CharField(max_length=15)

    def __str__(self):
        return self.post_type
