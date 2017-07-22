"""Create your tests here."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy
from imager_images.views import AddPhotoView, AddAlbumView
from imager_images.forms import PhotoForm, AlbumForm
from imager_images.models import Photo, Album
import factory
import faker
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import datetime
from bs4 import BeautifulSoup


HERE = os.path.dirname(__file__)
fake = faker.Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Creat photo factory."""

    class Meta:
        """."""

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
        """."""

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
        self.assertEqual(self.photo.published, "PB")

    def test_new_photo_choose(self):
        """Test assigned published status."""
        self.photo.published = 'PV'
        self.photo.save()
        self.assertEqual(self.photo.published, "PV")

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

    def test_upload_photo_instance(self):
        """Test upload photo with model properties."""
        photo = SimpleUploadedFile(
            name="MLKJR3.jpg",
            content=open(os.path.join(HERE, 'static', 'MLKJR3.jpg'), 'rb').read(),
            content_type="image/jpeg",
        )
        test_bob = User.objects.first()
        test_pic = Photo(
            user=test_bob,
            title="test_title",
            description="test_description",
            photo=photo
        )
        test_pic.save()
        self.assertIsInstance(test_pic.date_uploaded, datetime.date)
        self.assertTrue(test_pic.title == "test_title")
        self.assertTrue(test_pic.description == "test_description")
        self.assertTrue(test_pic.user.username == test_bob.username)

    def test_album_instance(self):
        """Test create album instance with user."""
        test_bob = User.objects.first()
        test_album = Album(
            user=test_bob,
            title="test_title",
            description="test_description"
        )
        test_album.save()
        self.assertTrue(test_album.user.username == test_bob.username)

    def test_photo_in_album(self):
        """Test create photo instance with album."""
        photo = SimpleUploadedFile(
            name="MLKJR3.jpg",
            content=open(os.path.join(HERE, 'static', 'MLKJR3.jpg'), 'rb').read(),
            content_type="image/jpeg",
        )
        test_bob = User.objects.first()
        test_album = Album(
            title="test_album_title",
            user=test_bob
        )
        test_pic = Photo(
            user=test_bob,
            title="test_photo_title",
            description="test_description",
            photo=photo
        )
        test_pic.save()
        test_album.save()
        test_pic.album.add(test_album)
        self.assertTrue(test_album.photos.first().title == test_pic.title)


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
        self.assertEqual(self.album_one.published, "PB")

    def test_new_album_choose(self):
        """Test assigned published status."""
        self.album_one.published = 'PV'
        self.assertEqual(self.album_one.published, "PV")

    def test_delete_user_with_albums_albums_removed(self):
        """Test delete user all objects."""
        self.assertTrue(Album.objects.count() == 6)
        self.user.delete()
        self.assertTrue(Album.objects.count() == 0)


class TemplatesTests(TestCase):
    """."""

    def setUp(self):
        """."""
        self.client = Client()
        user = User(
            username='fred',
            email='fred@fred.com'
        )
        user.set_password('temporary')
        user.save()
        self.user = user
        photos = [PhotoFactory.build() for i in range(20)]
        for photo in photos:
            photo.user = user
            photo.save()
        user.save()

    def test_to_libray_page_user_authenticated(self):
        """Test library page redirect."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get("/images/library/")

        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, 'imager_images/library.html')

    def test_to_photo_gallery_user_authenticated(self):
        """Test photo gallery page redirect."""
        self.client.login(username='Fred', password='temporary')
        idx = self.user.photobuild.first().id
        response = self.client.get("/images/photos/{}/".format(idx))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/photo_indiv.html')

    def test_to_album_gallery_user_authenticated(self):
        """Test album gallery page redirect."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get("/images/albums/")
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, 'imager_images/album_gallery.html')

    def test_when_no_image(self):
        """Placeholder appears with default image."""
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(html.find('image', {'src': "/MEDIA/user_images/animate0.png"}))

    def test_route_lists_images(self):
        """Test profile page redirect."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get("/profile/")
        self.assertTrue(response.status_code == 200)

    def test_add_photo_form(self):
        """Test add photo form."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get("/images/photos/add/")
        the_form = PhotoForm.base_fields
        self.assertTrue('title' in the_form)
        self.assertTrue(response.status_code == 200)

    def test_add_album_form(self):
        """Test add album form."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get("/images/albums/add/")
        the_form = AlbumForm.base_fields
        self.assertTrue('title' in the_form)
        self.assertTrue(response.status_code == 200)

    def test_when_at_least_one_image(self):
        """Placeholder appears with at least one image."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/images/library/')
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(len(html.find_all('img')) == 20)
