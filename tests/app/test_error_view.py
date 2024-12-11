from django.test import TestCase, Client


class ErrorViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_handler404(self):
        # Attempt to access a non-existent page
        response = self.client.get('/non-existent-page/')

        # Check that the response is 404
        self.assertEqual(response.status_code, 404)

        # Check that the correct template is used
        self.assertTemplateUsed(response, '404.html')
