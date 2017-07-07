"""Create your tests here."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from imager_images.models import Photo, Album
import factory
import faker
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
    """Photo test case."""

    def setUp(self):
        """Setup user fred."""
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
        """Test new photo instance."""
        self.assertEqual(Photo.objects.count(), 1)

    def test_photo_assigned_to_test_bob(self):
        """Test that fred is photo builder."""
        test_bob = User()
        test_bob.username = 'test_bob'
        test_bob.save()
        test_photo = Photo(user=test_bob)
        test_photo.save()
        self.assertTrue(test_photo.user.username == "test_bob")

    def test_new_photo_is_private_by_default(self):
        """Test default published status."""
        self.assertEqual(self.photo.published, "PV")

    def test_new_photo_choose(self):
        """Test assigned published status."""
        self.photo.published = 'PB'
        self.photo.save()
        self.assertEqual(self.photo.published, "PB")

    def test_delete_user_with_photos_photos_removed(self):
        """Test delete user all objects."""
        self.user.delete()
        self.assertTrue(Photo.objects.count() == 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        """Test media upload."""
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
        directory_contents = os.listdir(upload_dir)
        name = self.photo.photo.name.split('/')[1]
        self.assertTrue(name in directory_contents)


class AlbumsTestCase(TestCase):
    """Album test case."""

    def setUp(self):
        """Setup user fred."""
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

    def test_upload_image_adds_new_album_instance(self):
        """Test new album instance."""
        self.assertEqual(Album.objects.count(), 6)

    def test_album_assigned_to_bob(self):
        """Test that fred is album builder."""
        test_bob = User()
        test_bob.username = 'test_bob'
        test_bob.save()
        test_album = Album(user=test_bob)
        test_album.save()
        self.assertTrue(test_album.user.username == "test_bob")

    def test_albums_created_are_private_by_default(self):
        """Test default published status."""
        self.assertEqual(self.album_one.published, "PV")

    def test_new_album_choose(self):
        """Test assigned published status."""
        self.album_one.published = 'PB'
        self.assertEqual(self.album_one.published, "PB")

    def test_delete_user_with_albums_albums_removed(self):
        """Test delete user all objects."""
        self.assertTrue(Album.objects.count() == 6)
        self.user.delete()
        self.assertTrue(Album.objects.count() == 0)
