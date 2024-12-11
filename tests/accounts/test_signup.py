from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


class SignupViewTest(TestCase):
    def setUp(self):
        # Create a temporary image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Prepare signup data
        self.signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Prepare profile data with a real image
        self.profile_data = {
            'profile_image': SimpleUploadedFile(
                name='test_profile.jpg',
                content=image_io.getvalue(),
                content_type='image/jpeg'
            )
        }

    def test_user_signup(self):
        # Combine signup and profile data
        signup_post_data = self.signup_data.copy()
        signup_post_data.update(self.profile_data)

        # Submit signup form
        response = self.client.post(reverse('signup user'), data=signup_post_data)

        # Check that user was created and redirected
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('current user profile'))

        # Verify user can log in
        self.assertTrue(self.client.login(username='newuser', password='TestPassword123!'))