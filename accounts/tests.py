from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Bookmark, UserFollowing
from blog.models import Post, Category

User = get_user_model()


class UserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="testemail@email.com", password="testpass123"
        )
        self.assertEqual(user.email, "testemail@email.com")
        self.assertIsNotNone(user.username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        super_user = User.objects.create_superuser(
            username="admin", email="admin@email.com", password="testpass123"
        )
        self.assertEqual(super_user.email, "admin@email.com")
        self.assertEqual(super_user.username, "admin")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)


class SignupPageTests(TestCase):
    def setUp(self):
        self.email = "newuser@email.com"
        self.password = "testpass123"
        self.url = reverse("account_signup")

    def test_signup_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_signup_form(self):
        response = self.client.post(
            self.url,
            data={"email": self.email, "password": self.password},
        )
        self.assertEqual(response.status_code, 200)


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testemail@email.com", password="testpass123"
        )

    def test_user_profile(self):
        user_profile = self.user.profile
        user_profile.title = "User title"
        user_profile.about = "About me is here"
        user_profile.save()

        self.assertIsNotNone(user_profile)
        self.assertEqual(user_profile.title, "User title")
        self.assertEqual(user_profile.about, "About me is here")
        self.assertEqual(user_profile.followers, [])
        self.assertEqual(user_profile.following, [])

    def test_user_follow(self):
        user2 = User.objects.create(
            username="testuser_2", email="testemail_2@email.com", password="testpass123"
        )
        # self.user follows user2
        UserFollowing.objects.create(user=self.user, user_following=user2)
        self.assertNotEqual(self.user.profile.following, [])
        self.assertIn(user2, self.user.profile.following)
        self.assertIn(self.user, user2.profile.followers)


class BookmarkTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse("accounts:bookmark")
        self.user = User.objects.create(
            username="testuser", email="testemail@email.com", password="testpass123"
        )
        category = Category.objects.create(name="Test Category")
        self.post = Post.objects.create(
            title="Test post",
            category=category,
            content="Post content",
            author=self.user,
        )

    def test_bookmark(self):
        # user must be authenticated
        response = self.client.post(
            self.url,
            data={"user": self.user, "post_id": self.post.id},
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            data={"user": self.user, "post_id": self.post.id},
        )
        self.assertEqual(response.status_code, 200)

        bookmark = Bookmark.objects.get(user=self.user)
        self.assertEqual(Bookmark.objects.count(), 1)
        self.assertEqual(bookmark.post.title, self.post.title)
        self.assertEqual(bookmark.user, self.user)
