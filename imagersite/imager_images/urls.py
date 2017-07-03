"""URLs for the imager_images app."""

from django.conf.urls import url
from . import views

app_name = 'imager_images'

urlpatterns = [
    url(r'^library/$', views.library_view, name="library"),
    url(r'^photos/$', views.photo_gallery_view, name="photos"),
    url(r'^photos/(?P<pk>\d+)/$', views.photo_indiv_view, name="photo"),
    url(r'^albums/$', views.album_gallery_view, name="albums"),
    url(r'^albums/(?P<pk>\d+)/$', views.album_indiv_view, name="album"),
]
