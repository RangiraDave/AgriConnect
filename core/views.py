from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from django.http import JsonResponse
from .models import Profile, Farmer, VerificationCode, Product, ProductRating
from .forms import AddProductForm, EditProductForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def homepage(request):
    """Render the homepage."""
    return render(request, 'core/home.html')


@login_required(login_url='/login/')
def logout_view(request):
    """Log out the user and redirect them to the login page."""
    logout(request)
    return redirect('login')


def login_view(request):
    """Render the login page and handle user authentication."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(username=email, password=password)

        if user and not user.email_verified:
            messages.error(request, _("Email not verified. Please check your email for the verification link."))
            return redirect('verify_email')

        if user:
            if hasattr(user, 'profile') and user.profile.role.strip().lower() == role.lower():
                login(request, user)
                if user.profile.role.lower() == 'cooperative':
                    return redirect('product_listings')
                return redirect('user_profile')
            else:
                messages.error(request, _("Invalid role provided."))
        else:
            messages.error(request, _("Invalid username or password!"))

    return render(request, 'auth/login.html')


@login_required
def cooperative_dashboard(request):
    """Render the cooperative dashboard."""
    return render(request, 'cooperative_dashboard.html')


def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return random.randint(100000, 999999)


def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        if not all([username, email, password, phone, role, confirm_password]):
            errors['general'] = _('All fields are required.')

        if password != confirm_password:
            errors['password'] = _('Passwords do not match.')

        if User.objects.filter(username=username).exists():
            errors['username'] = _('The username is already taken.')
        if User.objects.filter(email=email).exists():
            errors['email'] = _('The email is already in use.')
        if Profile.objects.filter(phone=phone).exists():
            errors['phone'] = _('The phone number is already in use.')

        if errors:
            return render(request, 'core/signup.html', {'errors': errors, 'form_data': request.POST})

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()

                verification_code = generate_verification_code()
                VerificationCode.objects.create(user=user, code=verification_code)

                send_mail(
                    _('AgriConnect Email Verification'),
                    _('Your verification code is: %(code)s') % {'code': verification_code},
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                Profile.objects.create(user=user, phone=phone, role=role)

                request.session['verification_email'] = email
                return redirect('verify_email')

        except Exception as e:
            logger.error(f"Error during signup: {e}")
            return render(request, 'core/signup.html', {'error': str(e)})

    return render(request, 'core/signup.html')


def verify_email(request):
    """Verify the email address of a user."""
    if request.method == 'POST':
        email = request.session.get('verification_email')
        verification_code = request.POST.get('verification_code')

        if not email:
            messages.error(request, _("No email found for this session. Please try resending the verification code."))
            return redirect('resend_verification')

        try:
            user = User.objects.get(email=email)
            code_instance = get_object_or_404(VerificationCode, user=user)

            if code_instance.code == verification_code.strip() and not code_instance.is_expired():
                user.email_verified = True
                user.is_active = True
                user.save()

                # Automatically log in the user after successful verification
                login(request, user)

                messages.success(request, _("Email verified successfully! You are now logged in."))
                return redirect('user_profile')  # Redirect to the user's profile page
            else:
                messages.error(request, _("Invalid or expired verification code. Please try again."))
        except User.DoesNotExist:
            messages.error(request, _("Invalid verification process. Please try again."))

    return render(request, 'core/verify_email.html')


def resend_verification_code(request):
    """Resend the verification code to the user's email."""
    if request.method != 'POST':
        return redirect('signup')

    email = request.POST.get('email', request.session.get('verification_email'))

    try:
        user = User.objects.get(email=email)
        if user.email_verified:
            messages.info(request, _("Your email is already verified."))
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

    except User.DoesNotExist:
        messages.error(request, _("Email not found. Please try again."))

    return render(request, 'core/verify_email.html')


@login_required
def product_listings(request):
    """Display a list of all products."""
    products = Product.objects.select_related('owner').all()
    context = {
        'products': products,
        'welcome_message': _("Murakaza neza kurubuga rwa AgriConnect!"),
        'user_count': User.objects.count(),
        'total_products': len(products),
    }
    return render(request, 'core/product_listings.html', context)


@login_required(login_url='/login/')
def add_product(request):
    """Handle the form submission for adding a product."""
    if request.user.profile.role.lower() not in ["umuhinzi", "cooperative"]:
        messages.error(request, _("You are not authorized to add a product."))
        return redirect('product_listings')

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    instance = form.save(commit=False)
                    instance.owner = request.user
                    instance.save()
                    messages.success(request, _("Product added successfully!"))
                    return redirect('product_listings')
            except Exception as e:
                logger.error(f"Error while saving product: {e}")
                messages.error(request, _("An error occurred while saving the product."))
        else:
            logger.debug(f"Form validation errors: {form.errors}")

    form = AddProductForm()
    return render(request, 'core/add_product.html', {'form': form})


@login_required(login_url='/login/')
def user_profile(request):
    """Display the user profile."""
    profile = Profile.objects.get(user=request.user)
    products = Product.objects.filter(owner=request.user)
    context = {
        'profile': profile,
        'products': products,
        'product_count': products.count(),
    }
    return render(request, 'core/user_profile.html', context)


@login_required
def edit_product(request, pk):
    """Handle editing a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _("Product updated successfully!"))
            return redirect('user_profile')
    else:
        form = EditProductForm(instance=product)
    return render(request, 'core/edit_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    """Handle deleting a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.owner:
        messages.error(request, _("You are not authorized to delete this product."))
        return redirect('user_profile')

    if request.method == 'POST':
        product.delete()
        messages.success(request, _("Product deleted successfully!"))
        return redirect('user_profile')

    return render(request, 'core/delete_product.html', {'product': product})


@login_required
def rate_product(request, pk):
    """Handle product rating submission."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        rating = request.POST.get('rating')
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            messages.error(request, _("Please provide a valid rating between 1 and 5."))
            return redirect('product_listings')

        ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': int(rating)}
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{product.owner.id}",
            {
                "type": "rating_notification",
                "message": f"Your product '{product.name}' received a {rating}-star rating!"
            }
        )

        messages.success(request, _("Rating submitted successfully!"))
        return redirect('product_listings')

    return redirect('product_listings')


@login_required
def market_insights(request):
    """Display market insights including top-rated products and farmers."""
    top_products = Product.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        num_ratings=Count('ratings')
    ).filter(num_ratings__gt=0).order_by('-avg_rating', '-num_ratings')[:5]

    top_farmers = User.objects.filter(
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
    """Handle account deletion."""
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, _("Your account has been deleted successfully."))
        return redirect('homepage')

    return render(request, 'core/delete_account.html')
