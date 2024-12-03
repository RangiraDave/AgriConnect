from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model

    This model extends the default Django user model to include additional fields
    """

    ROLES = (
        ('umuhinzi', 'Umuhinzi'),
        ('umuguzi', 'Umuguzi'),
        ('cooperative', 'Cooperative'),
    )
    role = models.CharField(max_length=15, choices=ROLES)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Change related_name here
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Change related_name here
        blank=True,
    )

    def __str__(self):
        return self.username


from django.contrib.auth.backends import ModelBackend
class EmailAuthBackend(ModelBackend):
    """
    Email authentication backend

    This backend allows users to authenticate using their email address
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None


class Profile(models.Model):
    """
    Profile model

    This model is used to store additional information about the user
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Farmer(models.Model):
    """
    Farmer model

    This model is used to store information about farmers
    """

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Farmer {self.profile.user.username}"
