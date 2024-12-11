from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Travel_blog.accounts.models import Profile


class ProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        Profile.objects.create(user=self.user)

    def test_delete_profile_requires_login(self):
        """Test that delete profile view requires authentication"""
        response = self.client.get(reverse('delete profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        
        # More flexible URL checking
        self.assertTrue(
            '/accounts/views/signin/' in response.url or 
            '/accounts/signin/' in response.url,
            f"Unexpected redirect URL: {response.url}"
        )
        
        # Check for next parameter
        self.assertIn(f'next=/accounts/profile/{self.user.pk}/delete/', response.url)

    def test_delete_profile_post_request(self):
        """Test POST request to delete profile"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('delete profile', kwargs={'pk': self.user.pk})
        )
        
        # Check redirect to index
        self.assertRedirects(response, reverse('index'))
        
        # Verify user and profile are deleted
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(Profile.objects.filter(user=self.user).exists())