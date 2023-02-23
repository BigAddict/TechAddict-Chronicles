from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.models import Post


class User(AbstractUser):
    """Custom user model"""

    # additional user fields goes here
    pass


class Bookmark(models.Model):
    """Bookmark posts for later reading."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_bookmark")
        ]
