# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
import uuid


class CustomUser(AbstractUser):
    """
    Custom user model for general authentication details
    """
    email = models.EmailField(max_length=30, null=False, blank=False)
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
    code = models.CharField(max_length=6)  # 6-digit random code
    created_at = models.DateTimeField(auto_now_add=True)

    def default_expiry():
        """ Default expiry time for the code """
        return now() + timedelta(minutes=10)

    expires_at = models.DateTimeField(default=default_expiry)  # Code expires in 10 mins

    def is_expired(self):
        """ Check if the code has expired """
        return now() > self.expires_at

    def __str__(self):
        return f"{self.code}"

    def save(self, *args, **kwargs):
        """ Generate a 6-digit code if not provided """
        if not self.pk:
            self.code = str(uuid.uuid4())[:6] # Generate a 6-digit code on creation
        super(VerificationCode, self).save(*args, **kwargs)


class Profile(models.Model):
    """
    Profile model to store additional user details
    """
    ROLE_CHOICES = [
        ('umuhinzi', 'Umuhinzi'),
        ('umuguzi', 'Umuguzi'),
        ('cooperative', 'Cooperative'),
    ]

    bio = models.TextField(blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', unique=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=True, null=True)
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


from django.contrib.auth import get_user_model
User = get_user_model()


class Product(models.Model):
    """
    Product model to store produce details
    """
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Litre'),
        ('unit', 'Unit')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)  # Product name
    contact = models.CharField(max_length=25)  # Contact details
    description = models.TextField(blank=True, null=True)  # Product description
    media = models.FileField(upload_to='products/media/', blank=True, null=True)  # Image or video
    # location = models.CharField(max_length=255)  # Location where the product is available

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    #location fields for future geo-search:
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the Product model
        """
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
