"""Test User Registration Views."""

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from bs4 import BeautifulSoup


class RegistrationTests(TestCase):
    """."""

    def setUp(self):
        """."""
        self.client = Client()

    def test_registration_pages_uses_proper_template(self):
        """Test registration template."""
        response = self.client.get(reverse('registration_register'))
        self.assertIn('registration/registration_form.html', response.template_name)

    def test_upon_registration_create_new_user(self):
        """Test registration process."""
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')
        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']
        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'bob',
            'email': 'bob@bob.com',
            'password1': 'iambob_thebobbiest',
            'password2': 'iambob_thebobbiest',
        }
        response = self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertTrue(User.objects.count() == 1)

    def test_upon_registration_new_user_notactive(self):
        """Test registration process."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')
        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']
        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'bob',
            'email': 'bob@bob.com',
            'password1': 'iambob_thebobbiest',
            'password2': 'iambob_thebobbiest'
        }
        response = self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertFalse(User.objects.first().is_active)

    def test_valid_user_login(self):
        """Test login process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_invalid_user_login_blank_username(self):
        """Test login username is blank."""
        self.client.login(username='', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_invalid_user_login_blank_password(self):
        """Test login username is blank."""
        self.client.login(username='fred', password='')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_invalid_user_login_username(self):
        """Test login process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='bill', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


    def test_invalid_user_login_password(self):
        """Test login process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='fred', password='temp')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


    def test_upon_user_logout(self):
        """Test logout process."""
        self.client.login(username='Sally', password='potatosalad')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
