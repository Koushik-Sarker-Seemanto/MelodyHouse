# Generated by Django 2.2.4 on 2019-10-17 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 11, 47, 42, 276970)),
        ),
        migrations.AddField(
            model_name='song',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 11, 47, 42, 277601)),
        ),
    ]