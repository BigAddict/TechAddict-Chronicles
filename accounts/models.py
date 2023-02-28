from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.models import Post


class User(AbstractUser):
    """Custom user model"""

    # additional user fields goes here
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user}'s profile"

    @property
    def following(self):
        """All users followed by this user (following wrt the user)."""
        return [f.user_following for f in self.user.following.all()]

    @property
    def followers(self):
        """All users following this user (follower wrt the user)."""
        return [f.user for f in self.user.followers.all()]


class Bookmark(models.Model):
    """Posts saved for later reading"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_bookmark")
        ]


class UserFollowing(models.Model):
    """
    Follower and Following relationship between users.

    user: current user
    user_following: target user current user is following
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    user_following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "user_following"], name="unique_follow"
            )
        ]
