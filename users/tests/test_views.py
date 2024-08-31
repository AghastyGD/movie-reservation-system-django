from django.test import TestCase
from django.urls import reverse
from users.models import User

class SignUpViewTests(TestCase):
    def test_signup_view_get(self):
        # Test if the view returns the correct template
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_view_post_success(self):
        # Test form behaviour on successful submission
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302) # Redirect after success
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_view_post_invalid(self):
        # Test form behaviour on invalid submission
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'wrongpass321',
        })
        self.assertEqual(response.status_code, 200)  # Form should be re-displayed
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())
