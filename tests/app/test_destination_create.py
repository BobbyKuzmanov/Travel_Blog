from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Travel_blog.app.models import Destination, Category
from Travel_blog.app.forms.create import DestinationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


class CreateDestinationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.client.login(username='testuser', password='12345')

    def test_create_destination_success(self):
        # Create a simple image for upload
        test_image_path = os.path.join(settings.BASE_DIR, 'tests', 'test_image.jpg')

        # Ensure the test image exists
        if not os.path.exists(test_image_path):
            # Create a minimal test image if it doesn't exist
            from PIL import Image
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image.save(test_image_path)

        with open(test_image_path, 'rb') as img:
            image = SimpleUploadedFile(
                name='test_image.jpg',
                content=img.read(),
                content_type='image/jpeg'
            )

        destination_data = {
            'title': 'Test Destination',
            'description': 'A wonderful travel story',
            'country': 'Test Country',
            'year': 2022,
            'category': self.category.id,
        }

        # Prepare multipart form data
        destination_data_with_file = destination_data.copy()
        destination_data_with_file['image'] = image

        # Print out detailed debugging information
        print("\n--- Debugging Information ---")
        print("Destination Data:", destination_data)
        print("Category ID:", self.category.id)
        print("User:", self.user.username)

        # Attempt to validate form manually first
        form = DestinationForm(destination_data)
        print("Form Validation (Without Image):", form.is_valid())
        if not form.is_valid():
            print("Form Errors (Without Image):", form.errors)

        # Make the POST request
        response = self.client.post(
            reverse('destination create'),
            destination_data_with_file,
            format='multipart'
        )

        # Print response details
        print("Response Status Code:", response.status_code)

        # If response is 200, print form errors
        if response.status_code == 200:
            context_form = response.context.get('form')
            if context_form:
                print("Context Form Errors:", context_form.errors)
                print("Context Form Valid:", context_form.is_valid())

        # Print response content for further investigation
        print("Response Content:", response.content.decode('utf-8'))

        # Check redirect to destination list
        try:
            self.assertRedirects(response, reverse('destination list'))
        except AssertionError:
            print("Redirection Failed")
            raise

        # Verify destination was created
        destination = Destination.objects.first()
        self.assertIsNotNone(destination)
        self.assertEqual(destination.user, self.user)
        self.assertEqual(destination.title, 'Test Destination')

    def test_create_destination_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('destination create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
