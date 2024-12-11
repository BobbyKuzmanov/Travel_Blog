from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Travel_blog.app.models import Destination, Category, Like
from django.core.files.uploadedfile import SimpleUploadedFile


class DestinationLikesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')

        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )

        self.destination = Destination.objects.create(
            title='Test Destination',
            description='Test Description',
            country='Test Country',
            year=2022,
            category=self.category,
            user=self.user,
            image=test_image
        )

    def test_destination_like_toggle(self):
        self.client.login(username='testuser', password='12345')

        # Like the destination
        like_url = reverse('destination likes', kwargs={'pk': self.destination.pk})
        response = self.client.get(like_url)

        # Check that a like was created
        self.assertTrue(Like.objects.filter(
            user=self.user,
            destination=self.destination
        ).exists())

        # Unlike the destination
        response = self.client.get(like_url)

        # Check that the like was removed
        self.assertFalse(Like.objects.filter(
            user=self.user,
            destination=self.destination
        ).exists())
