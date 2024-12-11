from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Travel_blog.app.models import Destination, Category
from django.core.files.uploadedfile import SimpleUploadedFile


class DestinationListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content is fine for this test
            content_type='image/jpeg'
        )
        
        Destination.objects.create(
            title='Test Destination',
            description='Test Description',
            country='Test Country',
            year=2022,
            category=self.category,
            user=self.user,
            image=test_image
        )

    def test_destination_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('destination list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/destination_list.html')