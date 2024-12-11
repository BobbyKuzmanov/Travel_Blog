from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SignOutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signout_url = reverse('signout user')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_signout_authenticated_user(self):
        # First login the user
        self.client.login(username='testuser', password='testpass123')
        # Verify user is logged in
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Now test logout
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('index'))
        # Verify user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_signout_unauthenticated_user(self):
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('index'))
