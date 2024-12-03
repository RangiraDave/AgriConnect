from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender='core.CustomUser')
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a new user is created

    Args:
        sender: The sender of the signal
        instance: The instance of the sender
        created: A boolean value indicating if the instance was created
        **kwargs: Additional keyword arguments

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender='core.CustomUser')
def save_profile(sender, instance, **kwargs):
    """
    Save the profile when the user is saved.
    """
    instance.profile.save()
