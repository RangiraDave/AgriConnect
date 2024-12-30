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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)  # Product name
    contact = models.CharField(max_length=25)  # Contact details
    description = models.TextField(blank=True, null=True)  # Product description
    media = models.FileField(upload_to='products/media/', blank=True, null=True)  # Image or video
    # location = models.CharField(max_length=255)  # Location where the product is available

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('l', 'Litre'), ('unit', 'Unit')])

    #location fields for future geo-search:
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.owner.name}"


# Chat and Notification models
class ChatRoom(models.Model):
    """
    ChatRoom model to store chat room details
    """
    name = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    paticipants = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Message model to store chat messages
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"


class PrivateConversation(models.Model):
    """
    PrivateConversation model to store private chat details
    """
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_conversations')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_conversations')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"

    class Meta:
        unique_together = ['user1', 'user2']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message[:20]}...'
