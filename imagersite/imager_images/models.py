"""Create your models here."""

from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


PUBLISHED_STATUS = (
    ('PB', 'public'),
    ('PV', 'private'),
    ('SH', 'shared'),
)


class PhotoManager(models.Manager):
    """Manage photos."""

    def get_queryset(self):
        """Return published photos."""
        return super(PhotoManager, self).get_queryset().filter(published="PB").all()


class Photo(models.Model):
    """Create a photo model."""

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PB'
    )
    user = models.ForeignKey(
        User,
        related_name="photobuild",
        null=False,
        on_delete=models.CASCADE
    )
    photo = models.ImageField(
        upload_to='user_images',
        null=True
    )

    objects = models.Manager()
    published_photos = PhotoManager()

    def __repr__(self):
        """Print photo name."""
        return "<Photo: {}>".format(self.title)

    def __str__(self):
        """Print photo name."""
        return self.__repr__()


class AlbumManager(models.Manager):
    """Manage albums."""

    def get_queryset(self):
        """Return published albums."""
        return super(AlbumManager, self).get_queryset().filter(published="PB").all()


class Album(models.Model):
    """Create an album model."""

    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(
        max_length=2,
        choices=PUBLISHED_STATUS,
        default='PB'
    )
    user = models.ForeignKey(
        User,
        related_name="albumbuild",
        null=False,
        on_delete=models.CASCADE
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='album'
    )
    cover = models.ForeignKey(
        Photo,
        null=True,
        related_name="+"
    )
    objects = models.Manager()
    published_albums = AlbumManager()

    def __repr__(self):
        """Print album name."""
        return "<Album: {}>".format(self.title)
