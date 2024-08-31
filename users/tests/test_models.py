from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
      
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')