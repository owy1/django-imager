"""Create add photo form."""


from django import forms
from imager_images.models import Photo, Album


class PhotoForm(forms.ModelForm):
    """Edit photo form."""

    class Meta:
        """."""

        model = Photo
        fields = ['title', 'description', 'date_published', 'photo']
        widgets = {
            'description': forms.Textarea()
        }


class AlbumForm(forms.ModelForm):
    """Edit photo form."""

    class Meta:
        """."""

        model = Album
        fields = ['title', 'description', 'cover', 'date_published', 'photos']
        widgets = {
            'description': forms.Textarea()
        }