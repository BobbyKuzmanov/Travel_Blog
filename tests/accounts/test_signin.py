from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SignInViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('signin user')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_signin_GET(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signin.html')

    def test_signin_POST_success(self):
        response = self.client.post(self.signin_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signin_POST_invalid_credentials(self):
        response = self.client.post(self.signin_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertFalse(response.wsgi_request.user.is_authenticated)
