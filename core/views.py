# views.py
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _, gettext_lazy as _lazy
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
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Farmer, VerificationCode, Product, ProductRating
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
from django.urls import reverse_lazy
from django.db import IntegrityError, transaction
from .forms import AddProductForm, EditProductForm
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Avg, Count


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


@login_required(login_url='/login/')
def logout_view(request):
    """
    Log out the user and redirect them to the login page
    """
    logout(request)
    return redirect('login')


def login_view(request):
    """
    Render the login page

    If the request method is POST, get the user details from the form and authenticate the user.
    If the user is authenticated, login the user and redirect them to their respective dashboard.
    If the user is not authenticated, return an error message.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Use get to avoid KeyError
        
        logger.debug(f"Attempting to login: Username - {email}, Password - {password}, Role - {role}")
        
        user = authenticate(username=email, password=password)

        logger.debug(f"User authentication result: {user}")

        if user and not user.email_verified:
            messages.error(request, _("Email not verified. Please check your email for the verification link."))
            return redirect('verify_email')

        if user:
            print(f"Authenticating a User with email: {email}.")
            if hasattr(user, 'profile'):
                user_role = user.profile.role.strip().lower()
                if user_role == role.lower():
                    login(request, user)
                    # Redirect to product listings if role is cooperative
                    if user_role == 'cooperative':
                        return redirect('product_listings')
                    # messages.success(request, f"Welcome back {user.username}!")
                    # print(f"Login successful for user: {username}")
                    return redirect('user_profile')
                else:
                    messages.error(request, _("Invalid role provided."))
            else:
                messages.error(request, _("Invalid username or password!"))
        return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')


def cooperative_dashboard(request):
    return render(request, 'cooperative_dashboard.html')


# Function to generate random verification code
def generate_verification_code():
    return random.randint(100000, 999999)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        # Check required fields
        if not all([phone, role, email, username, password, confirm_password]):
            errors['general'] = _('All fields are required.')

        # Check if passwords match
        if password != confirm_password:
            errors['password'] = _('Passwords do not match.')

        # Check for duplicate username or email
        if User.objects.filter(username=username).exists():
            errors['username'] = _('The username is already taken.')
        if User.objects.filter(email=email).exists():
            errors['email'] = _('The email is already in use.')
        if Profile.objects.filter(phone=phone).exists():
            errors['phone'] = _('The phone number is already in use.')

        # If there are errors, return to the form with errors
        if errors:
            return render(request, 'core/signup.html', {'errors': errors, 'form_data': request.POST})

        try:
            with transaction.atomic():
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Set user as inactive until email verification
                user.save()

                # Create and save the verification code
                verification_code = generate_verification_code()
                VerificationCode.objects.create(user=user, code=verification_code)

                # Send email verification code
                send_mail(
                    _('AgriConnect Email Verification'),
                    _('Your verification code is: %(code)s') % {'code': verification_code},
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                # Create the profile
                Profile.objects.create(user=user, phone=phone, role=role)

                # Mock sending the verification email
                logger.info(f"Verification code for {email}: {verification_code}")

                request.session['verification_email'] = email
                request.session['verification_code'] = verification_code
                return redirect('verify_email')  # Redirect to email verification page

        except Exception as e:
            return render(request, 'core/signup.html', {'error': str(e)})

    return render(request, 'core/signup.html')


def verify_email(request):
    """
    Verify the email address of a user.
    """
    if request.method == 'POST':
        email = request.session.get('verification_email')

        if not email:
            messages.error(request, _("No email found for this session."))
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
                # messages.success(request, _("Email verified successfully! You can now log in."))
                return redirect('login')
            else:
                messages.error(request, _(f"Invalid verification code. Your codes:{code_instance}, Codes you entered: {verification_code}"))
                # return render(request, 'core/verify_email.html')
        except CustomUser.DoesNotExist:
            messages.error(request, _("Invalid verification process."))
        
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
            # messages.info(request, _("Your email is already verified."))
            return redirect('login')

        VerificationCode.objects.filter(user=user).delete()
        new_code = VerificationCode.objects.create(user=user)

        send_mail(
            _('AgriConnect Email Verification - Resend'),
            _('Your new verification code is: %(code)s') % {'code': new_code.code},
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, _("A new verification code has been sent to your email."))
        return redirect('verify_email')

    except CustomUser.DoesNotExist:
        # messages.error(request, _("Email not found."))
        pass
    
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
        'welcome_message': _("Murakaza neza kurubuga rwa AgriConnect!"),
        'user_count': User.objects.count(),  # Just an example of additional data you might want to show
        'total_products': len(products),
        # You can add more contextual data here if needed
    }

    return render(request, 'core/product_listings.html', context)


@login_required(login_url='/login/')
def add_product(request):
    """
    Handle the form submission for adding a product.

    This view function handles the form submission for adding a product.
    It validates the form data and saves the product to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with product listings or redirection to product listing upon success.
    """

    if request.user.profile.role.lower() not in ["umuhinzi", "cooperative"]:
        messages.error(request, _("You are not authorized to add a product."))
        return redirect('product_listings')

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                with transaction.atomic():
                    instance = Product(**form.cleaned_data)
                    instance.owner = User.objects.get(id=request.user.id)  # Use get_object_or_404?
                    instance.save()
                    messages.success(request, _("Product added successfully!"))
                    return redirect('product_listings')

            except IntegrityError as e:
                logger.error(f"Integrity error during save: {str(e)}")
                # messages.error(request, _("A database integrity error occurred."))
                raise

            except Exception as e:
                logger.error(f"General error during save: {str(e)}")
                messages.error(request, _("An error occurred while saving a product: %(error)s") % {'error': e})
        else:
            logger.debug(f"Form Validation Errors: {form.errors}")

    else:
        logger.info("Invalid Form Submission")

    context = {'form': AddProductForm()}
    return render(request, 'core/add_product.html', context)


@login_required(login_url='/login/')
def user_profile(request):
    """
    Display the user profile.
    
    This view function fetches the user's profile details and renders them on a template.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: Rendered page with user profile details.
    """
    # Fetch the user's profile
    profile = Profile.objects.get(user=request.user)
    # Fetch the user's products
    products = Product.objects.filter(owner=request.user).select_related('owner')

    # Pass context to the template
    context = {
        'profile': profile,
        'name': request.user.username,
        'welcome_message': _("Welcome to your profile!"),
        'products': products,
        'product_count': len(products),
    }

    return render(request, 'core/user_profile.html', context)


def edit_product(request, pk):
    """
    This view handles editing a product by its primary key.
    """
    try:
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            form = EditProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                with transaction.atomic():
                    isinstance=form.save(commit=False)
                    isinstance.owner = request.user
                    isinstance.save()
                    messages.success(request, _("Product updated successfully!"))
                    return redirect(reverse_lazy('user_profile'))

    except Product.DoesNotExist:
        messages.error(request, _("Product not found."))
        return redirect('user_profile')

    else:
        form = EditProductForm(instance=product)

    context = {'form': form}
    return render(request, 'core/edit_product.html', context)


def delete_product(request, pk):
    """
    This view handles deleting a product by its primary key.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.owner:
        messages.error(request, _("You are not authorized to delete this product."))
        return redirect('user_profile')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                product.delete()
                messages.success(request, _("Product deleted successfully!"))
                return redirect(reverse_lazy('user_profile'))

        except Exception as e:
            messages.error(request, _("An error occurred while deleting the product: %(error)s") % {'error': e})
            raise

        except Exception as e:
            messages.error(request, _("An error occurred while deleting the product: %(error)s") % {'error': e})
            raise

    context = {'product': product}
    return render(request, 'core/delete_product.html', context)


@login_required
def rate_product(request, pk):
    """
    Handle product rating submission and send notification to product owner.
    """
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=pk)
            rating = request.POST.get('rating')
            
            if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
                messages.error(request, _("Please provide a valid rating between 1 and 5."))
                return redirect('product_listings')

            # Create or update the rating
            rating_obj, created = ProductRating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating}
            )

            # Send notification to product owner via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{product.owner.id}",
                {
                    "type": "rating_notification",
                    "message": f"Your product '{product.name}' received a {rating}-star rating!"
                }
            )

            messages.success(request, _("Rating submitted successfully!"))
            return redirect('product_listings')

        except Exception as e:
            messages.error(request, str(e))
            return redirect('product_listings')

    return redirect('product_listings')


@login_required
def market_insights(request):
    """
    Display market insights including top-rated products and farmers.
    """
    # Get top rated products
    top_products = Product.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        num_ratings=Count('ratings')
    ).filter(num_ratings__gt=0).order_by('-avg_rating', '-num_ratings')[:5]

    # Get top rated farmers (users with role 'umuhinzi')
    top_farmers = CustomUser.objects.filter(
        profile__role='umuhinzi'
    ).annotate(
        avg_product_rating=Avg('product__ratings__rating'),
        num_products=Count('product', distinct=True),
        num_ratings=Count('product__ratings', distinct=True)
    ).filter(num_products__gt=0).order_by('-avg_product_rating', '-num_ratings')[:5]

    context = {
        'top_products': top_products,
        'top_farmers': top_farmers,
    }

    return render(request, 'core/market_insights.html', context)


@login_required(login_url='/login/')
def delete_account(request):
    """
    Handle the account deletion.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, _("Your account has been deleted successfully."))
        return redirect('homepage')

    return render(request, 'core/delete_account.html')
