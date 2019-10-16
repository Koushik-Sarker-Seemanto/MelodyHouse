# Generated by Django 2.2.4 on 2019-10-16 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload_app', '0002_album_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=100)),
                ('song_file', models.CharField(max_length=500)),
                ('description', models.CharField(blank=True, default='', max_length=1000)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_app.Album')),
            ],
            options={
                'unique_together': {('song_file', 'album_id')},
            },
        ),
    ]