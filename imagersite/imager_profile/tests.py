from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from bs4 import BeautifulSoup
from imager_profile.models import ImagerProfile
from imager_profile.forms import ImagerProfileForm
from imagersite.views import home_view
import factory
# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        """Generate a User instance with Sequence dynamically create unique field values."""
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class ProfileTestCase(TestCase):
    """Test for the profile model."""
    def setUp(self):
        self.client = Client()
        self.req_factory = RequestFactory()
        users = [UserFactory.create() for i in range(20)]

        for user in users:
            user.set_password('foo')
            user.save()

        self.users = users

    def test_profiles_are_made(self):
        """Test twenty profiles are created."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profiles_are_active(self):
        """Test twenty profiles are active."""
        self.assertTrue(ImagerProfile.active.count() == 20)

    def test_profile_fields(self):
        """Test profile is created with designated fields."""
        test_bob = self.users[0]
        test_bob.profile.location = "Seattle"
        test_bob.profile.job = "farmer"
        test_bob.profile.website = "http://www.test_bob.com"
        test_bob.save()
        self.assertTrue(test_bob.profile.camera_type == "iphone")
        self.assertTrue(test_bob.profile.photography_style == "color")
        self.assertTrue(test_bob.profile.social_status == "peasant")
        self.assertTrue(test_bob.profile.location == "Seattle")
        self.assertTrue(test_bob.profile.job == "farmer")
        self.assertTrue(test_bob.profile.website == "http://www.test_bob.com")

    def test_link_on_homepage_appears(self):
        """Reverse home route to test home link exist."""
        response = self.client.get(reverse('home'))
        self.assertTrue(b'home' in response.content)

    def test_home_view_return_status_code_200(self):
        """Home View response is 200 OK."""
        response = self.client.get(reverse_lazy('home'))
        self.assertTemplateUsed(response, 'imagersite/home.html')
        # self.assertEqual(response.status_code, 200)

    def test_home_route_return_status_code_200(self):
        """Home route response is 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_if_not_authenticated_user_loginpage_appears(self):
        """Reverse home route to test login link exist."""
        response = self.client.get(reverse('home'))
        self.assertTrue(b'login' in response.content.lower())

    def test_if_authenticated_user_logout_appears(self):
        """Reverse home route to test logout link exist."""
        test_fred = self.users[1]
        test_fred = User(username='fred')
        test_fred.set_password('temporary')
        test_fred.save()
        test_fred.profile.job = "farmer"
        test_fred.profile.website = "http://www.test_fred.com"
        test_fred.save()
        self.client.post(reverse('login'), {'username': 'fred', 'password': 'temporary'})
        response = self.client.get(reverse('home'))
        self.assertFalse(b'login' in response.content.lower())
        self.assertTrue(b'logout' in response.content.lower())

    def test_if_authenticated_user_logout_disappears(self):
        """Reverse home route to test logout link exist."""
        test_bob = User(username='bob')
        test_bob.set_password('temporary')
        test_bob.save()
        self.client.post(reverse('login'), {'username': 'bob', 'password': 'temporary'})
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTrue(b'login' in response.content.lower())

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
        """Create a new user then assert the user has a profile."""
        user = UserFactory.create()
        profile = ImagerProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_there_are_as_many_users_in_profile(self):
        """Test the number of profile objects eqaul user objects."""
        self.assertEquals(len(User.objects.all()), len(ImagerProfile.objects.all()))

    def test_edit_user_form(self):
        """Test edit user form."""
        test_bob = User(username='bob')
        test_bob.set_password('temporary')
        test_bob.save()
        self.client.login(username='bob', password='temporary')
        response = self.client.get("/profile/edit/")
        the_form = ImagerProfileForm.base_fields
        self.assertTrue('website' in the_form)
        self.assertTrue(response.status_code == 200)
