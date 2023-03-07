from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Post, Comment

User = get_user_model()


class CategoryTests(TestCase):
    def test_category(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(len(category.post_set.all()), 0)


class PostTests(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="This is test post",
            content="This is post content",
            author=self.user,
            category=self.category,
        )

    def test_post_create(self):
        url = reverse("blog:post_create")
        post_data = {
            "title": "Post title",
            "content": "Post content",
            "category": self.category,
            "author": self.user,
        }
        # user must be authenticated
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 200)

    def test_post_update(self):
        update_url = reverse("blog:post_update", args=(self.post.slug,))
        post_data = {
            "id": 1,
            "title": "This is test post (updated)",
            "content": "This is post content (updated)",
            "category": self.category,
            "author": self.user,
        }

        # user must be authenticated
        response = self.client.post(update_url, data=post_data)
        self.assertEqual(response.status_code, 302)

        user2 = User.objects.create(
            username="User2", email="user2@email.com", password="testpass123"
        )
        # user must be authorized
        self.client.force_login(user2)
        response = self.client.post(update_url, data=post_data)
        self.assertEqual(response.status_code, 403)

        # owners can edit/update their own post
        self.client.force_login(self.user)
        response = self.client.post(update_url, data=post_data)
        self.assertEqual(response.status_code, 200)


class CommentTests(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="This is test post",
            content="This is post content",
            author=self.user,
            category=self.category,
        )

    def test_comment_create(self):
        comment = Comment.objects.create(post=self.post, author=self.user)
        self.assertEqual(comment.post, self.post)
        self.assertNotEqual(self.post.comments.all(), [])
