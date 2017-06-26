from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from imager_profile.models import ImagerProfile
from imager_profile.views import home_view

import factory
# Create your tests here.

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        """."""
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class ProfileTestCase(TestCase):
    """Test for the profile model."""
    def setUp(self):
        users = [UserFactory.create() for i in range(20)]

        for user in users:
            user.set_password('foo')
            user.save()

        self.users = users

    def test_every_profile_must_have_a_user(self):
        """Test for profile instance error message."""
        with self.assertRaises(Exception):
            patron = ImagerProfile()
            patron.save()

    def test_profile_with_user_prints_username(self):
        """Test for profile instance."""
        some_profile = ImagerProfile.objects.first()
        self.assertTrue(str(some_profile), some_profile.user.username)

    def test_new_user_has_a_profile(self):
        """."""
        user = UserFactory.create()
        profile = ImagerProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_there_are_as_many_users_in_profile(self):
        """."""
        self.assertEquals(len(User.objects.all()), len(ImagerProfile.objects.all()))
