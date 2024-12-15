# views.py
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
import random
import hashlib
import hmac
from django.conf import settings
from django.utils.crypto import get_random_string   
import base64
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from core.models import CustomUser
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Farmer, VerificationCode, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
from django.urls import reverse_lazy

"""
The homepage view function is used to render the home.html template.
The farmer_list view function is used to render the farmer_list.html template.
The signup view function is used to render the signup.html template.
The login view function is used to render the login.html template.
The umuhinzi_login view function is used to render the umuhinzi_login.html template.
The umuguzi_login view function is used to render the umuguzi_login.html template.
The cooperative_login view function is used to render the cooperative_login.html template.
The send_verification_code view function is used to send a verification code to the user email.
"""


logger = logging.getLogger(__name__)
User = get_user_model()
welcome_message = _("Welcome to AgriConnect!")

def homepage(request):
    """
    Render the homepage
    """

    return render(request, 'core/home.html')

def farmer_list(request):
    """
    Render the farmer list
    """

    farmers = Farmer.objects.all()
    return render(request, 'core/farmer_list.html', {'farmers': farmers})

def login_view(request):
    """
    Render the login page

    If the request method is POST, get the user details from the form and authenticate the user.
    If the user is authenticated, login the user and redirect them to their respective dashboard.
    If the user is not authenticated, return an error message.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # Use get to avoid KeyError
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'profile') and user.profile.role == role:
                login(request, user)
                messages.success(request, f"Welcome back {user.username}!")
                return redirect(reverse_lazy('product_listings'))
            else:
                messages.error(request, "Invalid role for this user.")
        else:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'auth/login.html', {'error': ''})

def farmer_dashboard(request):
    return render(request, 'farmer_dashboard.html')

def buyer_dashboard(request):
    return render(request, 'buyer_dashboard.html')

def cooperative_dashboard(request):
    return render(request, 'cooperative_dashboard.html')

def signup(request):
    """
    Handle the signup form submission and send verification email.
    """
    if request.method == 'POST':
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        # Check required fields
        if not all([phone, role, email, username, password, confirm_password]):
            errors['general'] = 'All fields are required.'

        # Check if passwords match
        if password != confirm_password:
            errors['password'] = 'Passwords do not match.'

        # Check for duplicate username or email
        if User.objects.filter(username=username).exists():
            errors['username'] = 'The username is already taken.'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'The email is already in use.'

        # If there are errors, return to the form with errors
        if errors:
            return render(request, 'core/signup.html', {'errors': errors, 'form_data': request.POST})

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_active = False  # Mark the user as inactive until verification
        user.save()

        # Check if a Profile already exists for the user
        if not Profile.objects.filter(user=user).exists():
            # Create a Profile for the user only if one doesn't already exist
            profile = Profile.objects.create(
                user=user,
                phone=phone,
                role=role,
            )
            # request.session['verification_email'] = user.email

        # Create a verification code
        verification_code = VerificationCode.objects.create(user=user)

        # Send verification email
        send_mail(
            'AgriConnect Email Verification',
            f'Your verification code is: {verification_code.code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        request.session['verification_email'] = user.email
        messages.success(request, 'Account created successfully! Please check your email for the verification code.')

        return redirect('verify_email')

    return render(request, 'core/signup.html')

def verify_email(request):
    logger.debug("Entering verify_email view function")
    if request.method == 'POST':
        email = request.session.get('verification_email')

        if not email:
            messages.error(request, "No email found for this session.")
            return render(request, 'core/verify_email.html')

        verification_code = request.POST.get('verification_code')

        try:
            user = CustomUser.objects.get(email=email,)
            code_instance = get_object_or_404(VerificationCode, user=user)

            logger.debug(f"Verification attempt with code: {verification_code}")
            if code_instance.code == verification_code and not code_instance.is_expired():
                user.email_verified = True
                user.is_active = True
                user.is_verified = True  # Allow profile creation
                user.save()
                messages.success(request, "Email verified successfully! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Invalid verification code.")
                # return render(request, 'core/verify_email.html')
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid verification process.")
        
        return render(request, 'core/verify_email.html')

    return render(request, 'core/verify_email.html')

def resend_verification_code(request):
    """
    Resend the verification code to the user email
    """
    if request.method != 'POST':
        return redirect('signup')

    email = request.POST.get('email', request.session.get('verification_email'))

    try:
        user = CustomUser.objects.get(email=email)
        if user.email_verified:
            messages.info(request, "Your email is already verified.")
            return redirect('login')

        VerificationCode.objects.filter(user=user).delete()
        new_code = VerificationCode.objects.create(user=user)

        send_mail(
            'AgriConnect Email Verification - Resend',
            f'Your new verification code is: {new_code.code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, "A new verification code has been sent to your email.")
        return redirect('verify_email')

    except CustomUser.DoesNotExist:
        messages.error(request, "Email not found.")
    
    return render(request, 'core/verify_email.html')

@login_required
def product_listings(request):
    """
    Display a list of all products from farmers and cooperatives.
    
    This view fetches all products associated with either farmers or cooperatives 
    (since both are represented by CustomUser) and renders them on a template.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with product listings.
    """
    # Fetch all products linked to any user (farmers or cooperatives)
    products = Product.objects.select_related('owner').all()

    # Pass context to the template
    context = {
        'products': products,
        'welcome_message': _("Welcome to AgriConnect's Product Listings!"),
        'user_count': User.objects.count(),  # Just an example of additional data you might want to show
        'total_products': len(products),
        # You can add more contextual data here if needed
    }

    return render(request, 'core/product_listings.html', context)
