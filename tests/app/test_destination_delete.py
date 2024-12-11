from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Travel_blog.app.models import Destination, Category
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class DestinationDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.category = Category.objects.create(name='Test Category')

        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content is fine for this test
            content_type='image/jpeg'
        )

        # Create a destination with an image
        self.destination = Destination.objects.create(
            title='Test Destination',
            description='Test Description',
            country='Test Country',
            year=2022,
            category=self.category,
            user=self.user,
            image=test_image
        )

        # Store the image path
        self.image_path = self.destination.image.path

    def test_destination_delete_removes_image(self):
        # Ensure the image file exists before deletion
        self.assertTrue(os.path.exists(self.image_path))

        # Delete the destination
        response = self.client.post(reverse('destination delete', kwargs={'pk': self.destination.pk}))

        # Check that the destination was deleted
        self.assertFalse(Destination.objects.filter(pk=self.destination.pk).exists())

        # Check that the image file was deleted
        self.assertFalse(os.path.exists(self.image_path))
