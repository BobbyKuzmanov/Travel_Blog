from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.db.models import QuerySet  

from Travel_blog.app.models import Destination, Category
from Travel_blog.accounts.models import Profile  
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


class ProfileViewTest(TestCase):
    def setUp(self):
        # Create two users for testing
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            email='test1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )

        # Create profiles for both users
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

        # Create a test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Category Description'
        )
        
        # Create a test image file
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        # Create a test destination for user1
        self.destination = Destination.objects.create(
            title='Test Destination',
            description='Test Description',
            country='Test Country',
            year=2023,
            category=self.category,
            image=self.image,
            user=self.user1
        )

    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication"""
        response = self.client.get(reverse('current user profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Update to match the actual redirect URL
        self.assertIn('/accounts/views/signin/', response.url)
        
        # Additional check for the next parameter
        self.assertIn('next=/accounts/profile/', response.url)

    def test_own_profile_view_GET(self):
        """Test viewing own profile"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('current user profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['profile_user'], self.user1)
        self.assertTrue(response.context['is_owner'])
        
        # Get the destinations from the context
        context_destinations = response.context['destinations']
        
        # Check if the destinations are a QuerySet
        self.assertTrue(isinstance(context_destinations, QuerySet))
        
        # Compare the destinations
        self.assertEqual(list(context_destinations), [self.destination])

    def test_other_user_profile_view_GET(self):
        """Test viewing another user's profile"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('user profile', kwargs={'pk': self.user2.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['profile_user'], self.user2)
        self.assertFalse(response.context['is_owner'])

    def test_nonexistent_profile_view(self):
        """Test viewing a profile that doesn't exist"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('user profile', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_profile_POST_own_profile(self):
        """Test updating own profile"""
        self.client.login(username='testuser1', password='testpass123')
        
        # Create a test image file
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        response = self.client.post(
            reverse('current user profile'),
            {
                'profile_picture': image,
                'bio': 'New test bio'
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('current user profile'))

    def test_profile_POST_other_user(self):
        """Test attempting to update another user's profile"""
        self.client.login(username='testuser1', password='testpass123')
        
        response = self.client.post(
            reverse('user profile', kwargs={'pk': self.user2.pk}),
            {
                'bio': 'Trying to change other user bio'
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('current user profile'))
