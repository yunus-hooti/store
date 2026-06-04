from django.test import TestCase
# Create your tests here.

class profileViewTest(TestCase):
    def test_profile_view(self):
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_profile_content(self):
        response = self.client.get("/profile/")
        self.assertContains(response,'پروفایل')