from django import forms
from upload_app.models import Album
from authentication.models import Account


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'description']

    widgets = {
        'artist': forms.TextInput(attrs={'class': 'form-control'}),
        'album_title': forms.TextInput(attrs={'class': 'form-control'}),
        'genre': forms.Select(attrs={'class': 'custom-select'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
    }
