from django import forms
from upload_app.models import Album, Song
from authentication.models import Account


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'album_logo', 'genre', 'description']

    widgets = {
        'artist': forms.TextInput(attrs={'class': 'form-control'}),
        'album_title': forms.TextInput(attrs={'class': 'form-control'}),
        'genre': forms.Select(attrs={'class': 'custom-select'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
    }


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'song_file', 'album_id', 'description']

    widgets = {
        'song_title': forms.TextInput(attrs={'class': 'form-control'}),
        'song_file': forms.TextInput(attrs={'class': 'form-control'}),
        'album_id': forms.Select(attrs={'class': 'custom-select'}),
        # 'album_id': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
    }

    def __init__(self, user, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields['album_id'].queryset = Album.objects.filter(user=user)

