"""Create your tests here."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from imager_images.models import Photo, Album
import factory
import faker
from imager_profile.models import ImagerProfile
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import datetime


HERE = os.path.dirname(__file__)


fake = faker.Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creat photo factory."""

    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "Photo{}".format(n))
    description = fake.text(254)
    date_modified = datetime.datetime.now()
    photo = SimpleUploadedFile(
        name="MLKJR3.jpg",
        content=open(os.path.join(HERE, 'static', 'MLKJR3.jpg'), 'rb').read(),
        content_type="image/jpeg",
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Creat album factory."""

    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "Album{}".format(n))
    description = fake.text(254)
    date_modified = datetime.datetime.now()


class PhotoTests(TestCase):

    def setUp(self):
        user = User(
            username='fred',
            email='fred@fred.com'
        )
        user.set_password('potatoes')
        user.save()
        self.user = user
        photo = PhotoFactory.build()
        photo.user = user
        photo.save()
        self.photo = photo

    def test_upload_image_adds_new_photo_instance(self):
        self.assertEqual(Photo.objects.count(), 1)

    def test_new_photo_is_private_by_default(self):
        self.assertEqual(self.photo.published, "PV")

    def test_new_photo_choose_PB(self):
        self.photo.published = 'PB'
        self.photo.save()
        self.assertEqual(self.photo.published, "PB")

    def test_delete_user_with_photos_photos_removed(self):
        self.user.delete()
        self.assertTrue(Photo.objects.count() == 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
        directory_contents = os.listdir(upload_dir)
        name = self.photo.photo.name.split('/')[1]
        self.assertTrue(name in directory_contents)


class AlbumsTestCase(TestCase):

    def setUp(self):
        user = User(
            username='fred',
            email='fred@fred.com'
        )
        user.set_password('potatoes')
        user.save()
        self.user = user
        photos = [PhotoFactory.build() for i in range(20)]
        for photo in photos:
            photo.user = user
            photo.save()

        self.albums = [AlbumFactory.build() for i in range(5)]
        for idx, album in enumerate(self.albums):
            album.user = user
            album.cover = photos[idx]
            album.save()
            album.photos.add(photos[idx])

        album_one = AlbumFactory.build()
        album_one.user = user
        album_one.save()
        self.album_one = album_one

    def test_albums_created_are_private_by_default(self):
        self.assertEqual(self.album_one.published, "PV")

    def test_new_album_choose_PB(self):
        self.album_one.published = 'PB'
        self.assertEqual(self.album_one.published, "PB")

    def test_delete_user_with_albums_albums_removed(self):
        self.assertTrue(Album.objects.count() == 6)
        self.user.delete()
        self.assertTrue(Album.objects.count() == 0)
