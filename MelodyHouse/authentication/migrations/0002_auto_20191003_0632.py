# Generated by Django 2.2.4 on 2019-10-03 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='fav_genre',
            field=models.CharField(choices=[('Rock', 'Rock'), ('Metal', 'Metal'), ('Romantic', 'Romantic'), ('Heavy Metal', 'Heavy Metal'), ('Jazz', 'Jazz'), ('Folk', 'Folk'), ('Rap', 'Rap')], max_length=50),
        ),
    ]
