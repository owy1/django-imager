"""Imager_image View."""


from imager_images.models import Album, Photo
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.


class LibraryView(LoginRequiredMixin, TemplateView):
    """Display library view."""

    template_name = "imager_images/templates/library.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        """Library view context data."""
        user = self.request.user
        album_list = user.albumbuild.all()
        photo_list = user.photobuild.all()
        return
        {
            "albums": album_list,
            "photos": photo_list,
        }


class PhotoGalleryView(ListView):
    """Display photo gallery view."""

    template_name = "imager_images/templates/photo_gallery.html"
    model = Photo
    photos = Photo.published_photos.all()
    cotext_object_name = "photos"


class AlbumGalleryView(ListView):
    """Display album gallery view."""

    template_name = "imager_images/templates/album_gallery.html"
    model = Album
    context_object_name = "albums"

    def get_queryset(self):
        """Return specifc user album."""
        return Album.published_albums.filter(user=self.request.user)


class AddPhotoView(LoginRequiredMixin, CreateView):
    """Display addphoto view."""

    template_name = "imager_images/templates/add_photo.html"
    model = Photo
    login_url = reverse_lazy("login")
    fields = [
        "title", "description", "date_published", "photo"
    ]

    def form_valid(self, form):
        """User form."""
        form.instance.user = self.request.user
        photo = form.save()
        photo.user = self.request.user
        photo.save()
        return redirect("/images/library/")


class AddAlbumView(LoginRequiredMixin, CreateView):
    """Display addalbum view."""

    template_name = "imager_images/templates/add_album.html"
    model = Album
    login_url = reverse_lazy("login")
    fields = [
        "title", "description", "cover", "date_published", "photos"
    ]

    def form_valid(self, form):
        """User form."""
        form.instance.user = self.request.user
        album = form.save()
        album.user = self.request.user
        album.save()
        return redirect("/images/library/")
