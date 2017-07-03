"""Imager_image View."""


from imager_images.models import Album, Photo
from django.shortcuts import render
from django.http import HttpResponseForbidden


# Create your views here.


def library_view(request):
    """Display library view."""
    if request.user.is_authenticated():
        user = request.user
        album_list = user.albumbuild.all()
        photo_list = user.photobuild.all()
        return render(
            request,
            "library.html",
            {
                "albums": album_list,
                "photos": photo_list,
            }
        )
    return HttpResponseForbidden()


def photo_gallery_view(request):
    """Display photo gallery view."""
    if request.user.is_authenticated():
        photos = Photo.published_photos.all()
        return render(request, "photo_gallery.html", {"photos": photos})
    return HttpResponseForbidden()


def photo_indiv_view(request, pk):
    """Display photo detail view."""
    if request.user.is_authenticated():
        photo = Photo.objects.get(pk=pk)
        return render(request, "photo_indiv.html", {"photo": photo})
    return HttpResponseForbidden()


def album_gallery_view(request):
    """Display album gallery view."""
    if request.user.is_authenticated():
        albums = Album.published_albums.filter(user=request.user)
        return render(request, "album_gallery.html", {"albums": albums})
    return HttpResponseForbidden()


def album_indiv_view(request, pk):
    """Display album detail view."""
    if request.user.is_authenticated():
        album = Album.objects.get(pk=pk)
        photos = album.photos.all()
        return render(request, "album_indiv.html", {"photos": photos, "album": album})
    return HttpResponseForbidden()
