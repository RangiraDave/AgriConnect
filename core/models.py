# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
import uuid


class CustomUser(AbstractUser):
    """
    Custom user model for general authentication details
    """
    email = models.EmailField(max_length=255, null=False, blank=False)
    role = models.CharField(
        max_length=15,
        choices=[
            ('umuhinzi', 'Umuhinzi'),
            ('umuguzi', 'Umuguzi'),
            ('cooperative', 'Cooperative'),
        ],
    )
    is_verified = models.BooleanField(default=False)  # Track if the user is verified
    email_verified = models.BooleanField(default=False)  # Check if email is verified

    def __str__(self):
        return self.username

class VerificationCode(models.Model):
    """
    Model to store email verification codes
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6, default=str(uuid.uuid4().int)[:6])  # 6-digit random code
    created_at = models.DateTimeField(auto_now_add=True)

    def default_expiry():
        return now() + timedelta(minutes=10)

    expires_at = models.DateTimeField(default=default_expiry)  # Code expires in 10 mins

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"Verification Code for {self.user.email}"


class Profile(models.Model):
    """
    Profile model to store additional user details
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Farmer(models.Model):
    """
    Farmer-specific details, linked to Profile
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Farmer: {self.profile.name}"


class Buyer(models.Model):
    """
    Buyer-specific details
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Buyer: {self.profile.name}"


class Cooperative(models.Model):
    """
    Cooperative-specific details
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cooperative: {self.profile.name}"


class Product(models.Model):
    """
    Product model to store produce details
    """
    owner = models.ForeignKey(
        CustomUser,  # Links the product to the user (Farmer or Cooperative)
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)  # Product name
    description = models.TextField(blank=True, null=True)  # Product description
    media = models.FileField(upload_to='products/media/', blank=True, null=True)  # Image or video
    location = models.CharField(max_length=255)  # Location where the product is available
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.owner.name}"
