from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testemail@email.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testemail@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(
            username="superadmin", email="admin@email.com", password="testpass123"
        )
        self.assertEqual(super_user.username, "superadmin")
        self.assertEqual(super_user.email, "admin@email.com")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)


class SignupPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
