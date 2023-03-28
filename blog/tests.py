from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Post

User = get_user_model()


class HomePageTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/landing_page.html")
        self.assertTrue("featured_posts" in response.context)
        self.assertTrue("popular_categories" in response.context)


class PostViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 13  # create 13 posts for pagination tests
        category = Category.objects.create(name="Test Category")

        user = User.objects.create(username="testuser", email="testuser@email.com")
        user.set_password("testpass123")
        user.save()

        for id in range(number_of_posts):
            Post.objects.create(
                title=f"Post title {id}",
                content=f"Sample post content {id}",
                status=1,
                author=user,
                category=category,
            )

    def test_post_list_view(self):
        response = self.client.get("/stories/")
        self.assertEqual(response.status_code, 200)
        # accessible by name
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")
        self.assertIn("saved_posts", response.context)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["posts"]), 10)

        # test pagination on category view
        category = Category.objects.get(name="Test Category")
        response = self.client.get(reverse("blog:category", args=[category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/category.html")
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["category_posts"]), 10)

    def test_lists_all_posts(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse("blog:post_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["posts"]), 3)

        # test pagination on category view
        category = Category.objects.get(name="Test Category")
        response = self.client.get(
            reverse("blog:category", args=[category.slug]) + "?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["category_posts"]), 3)

    def test_post_detail_view(self):
        post = Post.objects.get(id=1)
        response = self.client.get(f"/p/{post.slug}/")
        self.assertEqual(response.status_code, 200)
        # accessible by name
        response = self.client.get(reverse("blog:post_detail", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertTrue("saved_posts" in response.context)

    def test_post_create_view(self):
        # user must be logged in
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next=/p/new/")

        login = self.client.login(email="testuser@email.com", password="testpass123")
        self.assertTrue(login)

        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_create.html")

    def test_post_update_view(self):
        # user must be logged in
        post = Post.objects.get(id=1)
        response = self.client.get(reverse("blog:post_update", args=[post.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next=/p/{post.slug}/edit/")

        login = self.client.login(email="testuser@email.com", password="testpass123")
        self.assertTrue(login)

        response = self.client.get(reverse("blog:post_update", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_update.html")
