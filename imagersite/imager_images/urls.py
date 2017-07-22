"""URLs for the imager_images app."""

from django.conf.urls import url
from django.views.generic import DetailView
from imager_images.models import Album, Photo
from imager_images.views import (
    LibraryView,
    PhotoGalleryView,
    AlbumGalleryView,
    AddPhotoView,
    AddAlbumView,
    EditAlbumView,
    EditPhotoView
)

app_name = 'imager_images'

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name="library"),
    url(r'^photos/$', PhotoGalleryView.as_view(), name="photos"),
    url(r'^photos/add/$', AddPhotoView.as_view(), name="add_photo"),
    url(r'^photos/(?P<pk>\d+)/edit/$', EditPhotoView.as_view(), name="edit_photo"),
    url(r'photos/(?P<pk>\d+)/$', DetailView.as_view(
        model=Photo,
        template_name="imager_images/photo_indiv.html",
        context_object_name="photo"
    ), name="photo"),
    url(r'^albums/$', AlbumGalleryView.as_view(), name="albums"),
    url(r'^albums/add/$', AddAlbumView.as_view(), name="add_album"),
    url(r'^albums/(?P<pk>\d+)/edit/$', EditAlbumView.as_view(), name="edit_album"),
    url(r'albums/(?P<pk>\d+)/$', DetailView.as_view(
        model=Album,
        template_name="imager_images/album_indiv.html",
        context_object_name="album"
    ), name="album")
]
