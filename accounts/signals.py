from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_profile(sender, instance, created, **kwargs):
    """
    Automatically create a user profile after sign up or
    update it whenever user information is updated.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
