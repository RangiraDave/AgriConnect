from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from .models import Profile, Farmer, VerificationCode, Product, ProductRating, Province, District, Sector, Cell, Village, Cooperative, Buyer
from .forms import AddProductForm, EditProductForm, ProfileEditForm, SignupForm, LoginForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import logging
from django.utils.timesince import timesince
from django.core.exceptions import ObjectDoesNotExist
import json

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
    """Render the login page and handle user authentication with reCAPTCHA v3."""
    if 'next' in request.GET and not request.user.is_authenticated:
        messages.info(request, _("Login required to access this page."))

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            # reCAPTCHA is validated by the form
            user = authenticate(username=email, password=password)

            if user and not user.email_verified:
                messages.error(request, _("Email not verified. Please check your email for the verification link."))
                return redirect('verify_email')

            if user:
                try:
                    if hasattr(user, 'profile') and user.profile and user.profile.role:
                        user_role = user.profile.role.strip().lower()
                        if user_role == role.lower():
                            login(request, user)
                            if user_role == 'cooperative':
                                return redirect('product_listings')
                            next_url = request.GET.get('next') or request.POST.get('next')
                            if next_url:
                                return redirect(next_url)
                            return redirect('user_profile')
                        else:
                            messages.error(request, _("Invalid role selected for this account."))
                    else:
                        messages.error(request, _("User profile not properly configured. Please contact support."))
                except AttributeError:
                    messages.error(request, _("User profile not properly configured. Please contact support."))
            else:
                messages.error(request, _("Invalid username or password!"))
        else:
            # If reCAPTCHA or form is invalid, show a simple error
            messages.error(request, _("Please verify you are human and fill all fields correctly."))

    return render(request, 'auth/login.html', {'form': form})


@login_required
def cooperative_dashboard(request):
    """Render the cooperative dashboard."""
    return render(request, 'cooperative_dashboard.html')


def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return str(random.randint(100000, 999999))


def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']
            # Get location data
            province_id = request.POST.get('province')
            district_id = request.POST.get('district')
            sector_id = request.POST.get('sector')
            cell_id = request.POST.get('cell')
            village_id = request.POST.get('village')
            specific_location = request.POST.get('specific_location')
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.is_active = False
                    user.save()
                    # Generate verification code
                    verification_code = generate_verification_code()
                    logger.info(f"Generated verification code for {email}: {verification_code}")
                    VerificationCode.objects.filter(user=user).delete()
                    VerificationCode.objects.create(user=user, code=verification_code)
                    send_mail(
                        _('AgriConnect Email Verification'),
                        _('Your verification code is: %(code)s') % {'code': verification_code},
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    profile = Profile.objects.create(user=user, phone=phone, role=role)
                    if role == 'umuhinzi':
                        Farmer.objects.create(
                            profile=profile,
                            province_id=province_id,
                            district_id=district_id,
                            sector_id=sector_id,
                            cell_id=cell_id,
                            village_id=village_id,
                            specific_location=specific_location
                        )
                    elif role == 'cooperative':
                        Cooperative.objects.create(
                            profile=profile,
                            province_id=province_id,
                            district_id=district_id,
                            sector_id=sector_id,
                            cell_id=cell_id,
                            village_id=village_id,
                            specific_location=specific_location
                        )
                    elif role == 'umuguzi':
                        Buyer.objects.create(profile=profile)
                    request.session['verification_email'] = email
                    return redirect('verify_email')
            except Exception as e:
                logger.error(f"Error during signup: {e}")
                form.add_error(None, str(e))
        # If not valid or error, fall through to render with errors
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def verify_email(request):
    """Verify the email address of a user."""
    if request.method == 'POST':
        email = request.session.get('verification_email')
        verification_code = request.POST.get('verification_code', '').strip()

        logger.info(f"Verification attempt - Email: {email}, Code: {verification_code}")

        if not email:
            messages.error(request, _("No email found for this session. Please try resending the verification code."))
            return redirect('resend_verification')

        try:
            user = User.objects.get(email=email)
            code_instance = VerificationCode.objects.filter(user=user).order_by('-created_at').first()

            logger.info(f"Found verification code instance: {code_instance}")

            if not code_instance:
                messages.error(request, _("No verification code found. Please request a new one."))
                return redirect('resend_verification')

            if code_instance.code == verification_code:
                if not code_instance.is_expired():
                    user.email_verified = True
                    user.is_active = True
                    user.save()
                    code_instance.delete()
                    messages.success(request, _("Email verified successfully! You can now log in."))
                    return redirect('login')
                else:
                    logger.warning(f"Code expired for user {user.email}")
                    messages.error(request, _("Verification code has expired. Please request a new one."))
            else:
                logger.warning(f"Invalid code for user {user.email}. Expected: {code_instance.code}, Got: {verification_code}")
                messages.error(request, _("Invalid verification code. Please try again."))
        except User.DoesNotExist:
            logger.error(f"User not found for email: {email}")
            messages.error(request, _("Invalid verification process. Please try again."))

    return render(request, 'core/verify_email.html')


def resend_verification_code(request):
    """Resend the verification code to the user email."""
    if request.method != 'POST':
        return redirect('signup')

    email = request.POST.get('email', request.session.get('verification_email'))
    logger.info(f"Resending verification code to: {email}")

    if not email:
        messages.error(request, _("No email provided for verification."))
        return redirect('signup')

    try:
        user = User.objects.get(email=email)
        if user.email_verified:
            messages.info(request, _("Your email is already verified."))
            return redirect('login')

        # Delete any existing verification codes
        VerificationCode.objects.filter(user=user).delete()
        
        # Generate new verification code
        verification_code = generate_verification_code()
        logger.info(f"Generated new verification code for {email}: {verification_code}")
        
        # Create new verification code instance
        VerificationCode.objects.create(user=user, code=verification_code)

        # Send the new verification code via email
        send_mail(
            _('AgriConnect Email Verification - Resend'),
            _('Your new verification code is: %(code)s') % {'code': verification_code},
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # Set the email in session for later use in the verify_email view
        request.session['verification_email'] = email

        messages.success(request, _("A new verification code has been sent to your email."))
        return redirect('verify_email')

    except User.DoesNotExist:
        logger.error(f"User not found for email: {email}")
        messages.error(request, _("Email not found."))
        return redirect('signup')


@login_required
def product_listings(request):
    """Display all products with filtering and search capabilities."""
    # Get filter parameters
    search_query = request.GET.get('search', '')
    province_id = request.GET.get('province')
    district_id = request.GET.get('district')
    sector_id = request.GET.get('sector')
    cell_id = request.GET.get('cell')
    village_id = request.GET.get('village')

    # Start with all products
    products = Product.objects.all()

    # Apply search filter if provided
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply location filters
    try:
        if province_id and province_id != 'None':
            products = products.filter(
                Q(owner__profile__farmer__province_id=province_id) |
                Q(owner__profile__cooperative__province_id=province_id)
            )
        if district_id and district_id != 'None':
            products = products.filter(
                Q(owner__profile__farmer__district_id=district_id) |
                Q(owner__profile__cooperative__district_id=district_id)
            )
        if sector_id and sector_id != 'None':
            products = products.filter(
                Q(owner__profile__farmer__sector_id=sector_id) |
                Q(owner__profile__cooperative__sector_id=sector_id)
            )
        if cell_id and cell_id != 'None':
            products = products.filter(
                Q(owner__profile__farmer__cell_id=cell_id) |
                Q(owner__profile__cooperative__cell_id=cell_id)
            )
        if village_id and village_id != 'None':
            products = products.filter(
                Q(owner__profile__farmer__village_id=village_id) |
                Q(owner__profile__cooperative__village_id=village_id)
            )
    except Exception as e:
        messages.error(request, f"Error applying location filters: {str(e)}")
        products = Product.objects.all()  # Reset to all products on error

    # Get all provinces for the filter dropdown
    provinces = Province.objects.all()

    # Add a 'location' property to each product for display
    for product in products:
        if product.latitude and product.longitude:
            product.location = f"{product.latitude}, {product.longitude}"
        else:
            product.location = None

    context = {
        'products': products,
        'provinces': provinces,
        'total_products': products.count(),
        'selected_province': province_id,
        'selected_district': district_id,
        'selected_sector': sector_id,
        'selected_cell': cell_id,
        'selected_village': village_id,
    }

    return render(request, 'core/product_listings.html', context)


@login_required(login_url='/login/')
def add_product(request):
    """Handle the form submission for adding a product, including lat/lng."""
    if request.user.profile.role.lower() not in ["umuhinzi", "cooperative"]:
        messages.error(request, _("You are not authorized to add a product."))
        return redirect('product_listings')

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create instance but don't save to DB yet
                    instance = form.save(commit=False)
                    instance.owner = request.user

                    # Ensure the user has a profile phone number before saving
                    if not hasattr(request.user, 'profile') or not request.user.profile.phone:
                        messages.error(
                            request,
                            _("Please update your profile with contact information before adding a product.")
                        )
                        return redirect('edit_profile')

                    instance.save()

                    messages.success(request, _("Product added successfully!"))
                    return redirect('product_listings')

            except Exception as e:
                logger.error(f"Error while saving product: {e}")
                messages.error(
                    request,
                    _("An error occurred while saving the product. Please try again.")
                )
        else:
            logger.error(f"Form validation errors: {form.errors}")
            messages.error(request, _("Please correct the errors in the form."))

    else:
        form = AddProductForm()

    return render(request, 'core/add_product.html', {'form': form})


@login_required(login_url='/login/')
def user_profile(request):
    """Display the user profile."""
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, _("Your profile is not configured. Please contact support or log in again."))
        return redirect('login')
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
    if request.user != product.owner and request.user.profile.role.lower() not in ["umuhinzi", "cooperative"]:
        messages.error(request, _("You are not authorized to edit this product."))
        return redirect('product_listings')
        
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
    if request.user != product.owner and request.user.profile.role.lower() not in ["umuhinzi", "cooperative"]:
        messages.error(request, _("You are not authorized to delete this product."))
        return redirect('product_listings')

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

        # messages.success(request, _("Rating submitted successfully!"))
        return redirect('product_listings')

    return redirect('product_listings')


@login_required
def market_insights(request):
    """Display market insights including top-rated products and farmers."""
    # Calculate total products
    total_products = Product.objects.count()

    # Calculate active farmers (users with the role 'umuhinzi' who have at least one product)
    active_farmers = User.objects.filter(
        profile__role='umuhinzi',
        product__isnull=False
    ).distinct().count()

    # Calculate average rating across all products
    avg_rating = ProductRating.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    # Get top-rated products
    top_products = Product.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        num_ratings=Count('ratings')
    ).filter(num_ratings__gt=0).order_by('-avg_rating', '-num_ratings')[:5]

    # Serialize top products for JSON
    top_products_data = [
        {
            "name": str(product.name),
            "avg_rating": float(product.avg_rating or 0),
            "num_ratings": int(product.num_ratings),
        }
        for product in top_products
    ]

    # Get top-performing farmers with correct average rating calculation
    top_farmers = User.objects.filter(
        profile__role='umuhinzi',
        product__isnull=False
    ).annotate(
        total_products=Count('product', distinct=True),
        total_ratings=Count('product__ratings', distinct=True),
        avg_rating=Avg('product__ratings__rating')
    ).filter(total_ratings__gt=0).order_by('-avg_rating', '-total_ratings')[:5]

    # Serialize top farmers for JSON
    top_farmers_data = [
        {
            "username": str(farmer.username),
            "avg_rating": float(farmer.avg_rating or 0),
            "total_products": int(farmer.total_products),
            "total_ratings": int(farmer.total_ratings),
        }
        for farmer in top_farmers
    ]

    # Log the data for debugging
    logger.debug('Top products data: %s', top_products_data)
    logger.debug('Top farmers data: %s', top_farmers_data)

    context = {
        'total_products': total_products,
        'active_farmers': active_farmers,
        'avg_rating': avg_rating,
        'top_products': top_products,
        'top_products_json': top_products_data,
        'top_farmers': top_farmers,
        'top_farmers_json': top_farmers_data,
    }
    return render(request, 'core/market_insights.html', context)


@login_required(login_url='/login/')
def delete_account(request):
    """Handle account deletion."""
    if request.method == 'POST':
        request.user.delete()
        # messages.success(request, _("Your account has been deleted successfully."))
        return redirect('homepage')

    return render(request, 'core/delete_account.html')


def get_provinces(request):
    """AJAX endpoint to get all provinces"""
    provinces = Province.objects.all().values('id', 'name')
    return JsonResponse(list(provinces), safe=False)

def get_districts(request):
    """Get districts for a given province."""
    province_id = request.GET.get('province')
    if not province_id or province_id == 'None':
        return JsonResponse([], safe=False)
    
    try:
        districts = District.objects.filter(province_id=province_id).values('id', 'name')
        return JsonResponse(list(districts), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_sectors(request):
    """Get sectors for a given district."""
    district_id = request.GET.get('district')
    if not district_id or district_id == 'None':
        return JsonResponse([], safe=False)
    
    try:
        sectors = Sector.objects.filter(district_id=district_id).values('id', 'name')
        return JsonResponse(list(sectors), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_cells(request):
    """Get cells for a given sector."""
    sector_id = request.GET.get('sector')
    if not sector_id or sector_id == 'None':
        return JsonResponse([], safe=False)
    
    try:
        cells = Cell.objects.filter(sector_id=sector_id).values('id', 'name')
        return JsonResponse(list(cells), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_villages(request):
    """Get villages for a given cell."""
    cell_id = request.GET.get('cell')
    if not cell_id or cell_id == 'None':
        return JsonResponse([], safe=False)
    
    try:
        villages = Village.objects.filter(cell_id=cell_id).values('id', 'name')
        return JsonResponse(list(villages), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def product_list(request):
    """View for listing products with location-based filtering"""
    products = Product.objects.filter(is_available=True)
    
    # Get filter parameters
    province_id = request.GET.get('province')
    district_id = request.GET.get('district')
    sector_id = request.GET.get('sector')
    cell_id = request.GET.get('cell')
    village_id = request.GET.get('village')
    
    # Apply filters
    if province_id:
        products = products.filter(owner__farmer__province_id=province_id) | \
                  products.filter(owner__cooperative__province_id=province_id)
    if district_id:
        products = products.filter(owner__farmer__district_id=district_id) | \
                  products.filter(owner__cooperative__district_id=district_id)
    if sector_id:
        products = products.filter(owner__farmer__sector_id=sector_id) | \
                  products.filter(owner__cooperative__sector_id=sector_id)
    if cell_id:
        products = products.filter(owner__farmer__cell_id=cell_id) | \
                  products.filter(owner__cooperative__cell_id=cell_id)
    if village_id:
        products = products.filter(owner__farmer__village_id=village_id) | \
                  products.filter(owner__cooperative__village_id=village_id)
    
    # Get all provinces for the filter dropdown
    provinces = Province.objects.all()
    
    context = {
        'products': products,
        'provinces': provinces,
        'selected_province': province_id,
        'selected_district': district_id,
        'selected_sector': sector_id,
        'selected_cell': cell_id,
        'selected_village': village_id,
    }
    
    return render(request, 'core/product_list.html', context)

@login_required
def edit_profile(request):
    """View for editing user profile."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the profile first
            profile = form.save()
            
            # Handle location data for farmers and cooperatives
            if profile.role in ['umuhinzi', 'cooperative']:
                try:
                    location = getattr(profile, 'farmer', None) or getattr(profile, 'cooperative', None)
                    if not location and profile.role == 'umuhinzi':
                        # Create Farmer object if missing
                        from .models import Farmer
                        location = Farmer.objects.create(profile=profile)
                    elif not location and profile.role == 'cooperative':
                        from .models import Cooperative
                        location = Cooperative.objects.create(profile=profile)
                    if location:
                        # Update location data
                        location.province_id = form.cleaned_data.get('province')
                        location.district_id = form.cleaned_data.get('district')
                        location.sector_id = form.cleaned_data.get('sector')
                        location.cell_id = form.cleaned_data.get('cell')
                        location.village_id = form.cleaned_data.get('village')
                        location.specific_location = form.cleaned_data.get('specific_location')
                        location.save()
                except Exception as e:
                    messages.error(request, _('Error updating location information. Please try again.'))
                    return redirect('edit_profile')
            
            messages.success(request, _('Profile updated successfully.'))
            return redirect('user_profile')
    else:
        form = ProfileEditForm(instance=profile)
        # Set initial values for location fields if user is a farmer or cooperative
        if profile.role in ['umuhinzi', 'cooperative', 'umuguzi']:
            try:
                location = getattr(profile, 'farmer', None) or getattr(profile, 'cooperative', None)
                if not location and profile.role == 'umuhinzi':
                    # Create Farmer object if missing
                    from .models import Farmer
                    location = Farmer.objects.create(profile=profile)
                elif not location and profile.role == 'cooperative':
                    from .models import Cooperative
                    location = Cooperative.objects.create(profile=profile)
                if location:
                    form.fields['province'].initial = getattr(location, 'province_id', None)
                    form.fields['district'].initial = getattr(location, 'district_id', None)
                    form.fields['sector'].initial = getattr(location, 'sector_id', None)
                    form.fields['cell'].initial = getattr(location, 'cell_id', None)
                    form.fields['village'].initial = getattr(location, 'village_id', None)
                    form.fields['specific_location'].initial = getattr(location, 'specific_location', None)
            except Exception as e:
                messages.error(request, _('Error loading location information. Please try again.'))
                return redirect('user_profile')

    return render(request, 'core/edit_profile.html', {
        'form': form,
        'profile': profile
    })

def debug_db_config(request):
    """Temporary view to debug database configuration."""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Debug view not available in production'}, status=403)
    
    db_config = {
        'host': settings.DATABASES['default']['HOST'],
        'port': settings.DATABASES['default']['PORT'],
        'name': settings.DATABASES['default']['NAME'],
        'user': settings.DATABASES['default']['USER'],
        'password': '********' if settings.DATABASES['default']['PASSWORD'] else None,
    }
    return JsonResponse(db_config)

def product_detail(request, pk):
    """Display the details for a single product."""
    product = get_object_or_404(Product, pk=pk)
    time_since_added = timesince(product.created_at)
    return render(request, 'core/product_detail.html', {'product': product, 'time_since_added': time_since_added})
