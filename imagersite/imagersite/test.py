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
        html = BeautifulSoup(response.rendered_content)
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
        self.assertTrue(User.objects.count() == 1)

    def test_upon_registration_new_user_notactive(self):
        """Test registration process."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, from_encoding='utf-8')
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

    def test_upon_user_login(self):
        """Test login process."""
        user = User.objects.create_user(username='fred', email='test@test.com', password='temporary')
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_upon_user_logout(self):
        """Test logout process."""
        self.client.login(username='Sally', password='potatosalad')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
