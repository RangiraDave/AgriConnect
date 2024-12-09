# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
from core.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a new user is created
    """
    if created and instance.is_verified:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    """
    Save the profile when the user is saved
    """
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()
