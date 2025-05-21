# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
import uuid
import random
import os
from django.core.validators import FileExtensionValidator


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

    class Meta:
        ordering = ['id']


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
        """Check if the code has expired."""
        return now() > self.expires_at

    def __str__(self):
        return f"{self.code}"

    def save(self, *args, **kwargs):
        """ Only generate code if it's not provided """
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"  # Ensure 6-digit code
        super(VerificationCode, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']


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

    class Meta:
        ordering = ['id']


class Province(models.Model):
    """Model for Rwanda's provinces"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class District(models.Model):
    """Model for Rwanda's districts"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return f"{self.name}, {self.province.name}"

    class Meta:
        ordering = ['name']


class Sector(models.Model):
    """Model for Rwanda's sectors"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sectors')

    def __str__(self):
        return f"{self.name}, {self.district.name}"

    class Meta:
        ordering = ['name']


class Cell(models.Model):
    """Model for Rwanda's cells"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=8, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='cells')

    def __str__(self):
        return f"{self.name}, {self.sector.name}"

    class Meta:
        ordering = ['name']


class Village(models.Model):
    """Model for Rwanda's villages"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='villages')

    def __str__(self):
        return f"{self.name}, {self.cell.name}"

    class Meta:
        ordering = ['name']


class Farmer(models.Model):
    """
    Farmer-specific details, linked to Profile
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name='farmers')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='farmers')
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='farmers')
    cell = models.ForeignKey(Cell, on_delete=models.SET_NULL, null=True, related_name='farmers')
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, related_name='farmers')
    specific_location = models.CharField(max_length=255, blank=True, null=True, 
                                       help_text="Additional location details (e.g., house number, landmark)")

    def __str__(self):
        return f"Farmer: {self.profile.name}"

    class Meta:
        ordering = ['id']


class Buyer(models.Model):
    """
    Buyer-specific details
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Buyer: {self.profile.name}"

    class Meta:
        ordering = ['id']


class Cooperative(models.Model):
    """
    Cooperative-specific details
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name='cooperatives')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='cooperatives')
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='cooperatives')
    cell = models.ForeignKey(Cell, on_delete=models.SET_NULL, null=True, related_name='cooperatives')
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, related_name='cooperatives')
    specific_location = models.CharField(max_length=255, blank=True, null=True,
                                       help_text="Additional location details (e.g., office number, landmark)")

    def __str__(self):
        return f"Cooperative: {self.profile.name}"

    class Meta:
        ordering = ['id']


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
    description = models.TextField(blank=True, null=True)  # Product description
    media = models.FileField(
        upload_to='products/%Y/%m/%d/',  # Organize files by date
        blank=True, 
        null=True,
        help_text="Upload an image (jpg, png) or video (mp4)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4']),
        ]
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    quantity_available = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    contact = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number for this product (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

    def is_video(self):
        """Check if the media is a video file"""
        if self.media:
            return self.media.name.lower().endswith('.mp4')
        return False

    def save(self, *args, **kwargs):
        # Delete old file when updating
        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
                if old_instance.media and old_instance.media != self.media:
                    if os.path.isfile(old_instance.media.path):
                        os.remove(old_instance.media.path)
            except Product.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file when the product is deleted
        if self.media:
            if os.path.isfile(self.media.path):
                os.remove(self.media.path)
        super().delete(*args, **kwargs)

    @property
    def contact_number(self):
        """Get contact information for the product"""
        if self.contact:
            return self.contact
        try:
            return self.owner.profile.phone
        except:
            return None


class ProductRating(models.Model):
    """
    Stores ratings for a Product from a specific buyer.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(default=1) # Ratings from 1 to 5

    class Meta:
        """
        Meta class for the ProductRating model
        """
        unique_together = ['product', 'user']
        verbose_name = 'Product Rating'
        verbose_name_plural = 'Product Ratings'
        ordering = ['id']

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} {self.rating} stars"
