#!/usr/bin/env python3
import os
from django.core.mail import send_mail
from django.conf import settings

# Set up Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriConnect.settings')  # Replace 'AgriConnect.settings' with the correct path to your settings module

# Initialize Django
import django
django.setup()

# Test email
send_mail(
    subject='AgriConnect Email Test',
    message='This is a test email from AgriConnect.',
    from_email='rangiradave6@gmail.com',  # Change to match your sender email
    recipient_list=['rangiradev666@gmail.com'],  # Replace with your test email
    fail_silently=False,
)

