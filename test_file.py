from django.test import TestCase
from django.db.utils import IntegrityError
from account.models import User


# Create your tests here.

class profileViewTest(TestCase):
    def setUp(self):
        """
        create user
        """
        self.user = User.manager.create_user(phone="09153451234", password="password123")

    def test_profile_view(self):
        """
        Return code 200 to enter the profile
        """
        self.client.login(phone="09153451234", password="password123")
        response = self.client.get("/account/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_content(self):
        """
        is the word profile in the profile
        """
        self.client.login(phone="09153451234", password="password123")

        response = self.client.get("/account/profile/")
        self.assertContains(response, 'پروفایل')

    def test_profile_requires_login(self):
        """
        Request access to the profile without logging in and transfer to the login panel
        """
        response = self.client.get('/account/profile/')
        self.assertRedirects(response, '/account/login/')

    def test_profile_show_correct_user_data(self):
        """
        Not providing user information in another user`s panel
        """
        user_a = User.manager.create_user(phone="09153451231", password="password123")
        user_b = User.manager.create_user(phone="09153451235", password="password1234")
        self.client.login(phone="09153451231", password="password123")
        response = self.client.get('/account/profile/')
        self.assertContains(response, user_a.phone)
        self.assertNotContains(response,user_b.phone)

    def test_register(self):
        """
        Register a user with a duplicate number
        """
        User.manager.create_user(phone="09153451232", password="password123")

        with self.assertRaises(IntegrityError):
            User.manager.create_user(phone="09153451232", password="password123")
