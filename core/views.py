from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
import random
import json
from django.core.mail import send_mail
from django.http import JsonResponse
# from django.contrib.auth.models import User
from core.models import CustomUser
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile


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

def signup(request):
    """
    Render the signup page
    """

    return render(request, 'core/signup.html')

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
        role = request.POST['role']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.profile.role == role:
                login(request, user)
                if role == 'umuhinzi':
                    return redirect('umuhinzi_dashboard')
                elif role == 'umuguzi':
                    return redirect('umuguzi_dashboard')
                elif role == 'cooperative':
                    return redirect('cooperative_dashboard')
            else:
                return render(request, 'auth/login.html', {'error': 'Invalid role for this user!'})
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password!'})

    return render(request, 'auth/login.html')

def login_umuhinzi(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.profile.role == 'umuhinzi':
            login(request, user)
            return redirect('umuhinzi_dashboard')  # Redirect to umuhinzi dashboard
        else:
            messages.error(request, "Invalid credentials or role.")
    return render(request, 'auth/login_umuhinzi.html')

def login_umuguzi(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.profile.role == 'umuguzi':
            login(request, user)
            return redirect('umuguzi_dashboard')  # Redirect to umuguzi dashboard
        else:
            messages.error(request, "Invalid credentials or role.")
    return render(request, 'auth/login_umuguzi.html')

def login_cooperative(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.profile.role == 'cooperative':
            login(request, user)
            return redirect('cooperative_dashboard')  # Redirect to cooperative dashboard
        else:
            messages.error(request, "Invalid credentials or role.")
    return render(request, 'auth/login_cooperative.html')

def farmer_dashboard(request):
    return render(request, 'farmer_dashboard.html')

def buyer_dashboard(request):
    return render(request, 'buyer_dashboard.html')

def cooperative_dashboard(request):
    return render(request, 'cooperative_dashboard.html')

def signup(request):
    """
    Handle the signup form submission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        verification_code = request.POST.get('verification_code')

        # Validate input fields
        if not all([name, phone, role, email, password, confirm_password, verification_code]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        # Validate verification code
        session_code = request.session.get('verification_code')
        if session_code != verification_code:
            return JsonResponse({'error': 'Invalid verification code.'}, status=400)

        # Create and save the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = True
        user.save()

        # Save the profile
        profile = Profile.objects.create(user=user, name=name, phone=phone, role=role)
        profile.save()

        # Redirect to a success page or dashboard
        return redirect('login')

    return render(request, 'core/signup.html')

# @csrf_exempt
# def send_verification_code(request):
#     """
#     Send a verification code to the user's email.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             email = data.get('email')

#             if not email:
#                 return JsonResponse({'error': 'Email is required.'}, status=400)

#             # Simulate sending a verification code (or implement actual email sending)
#             verification_code = "123456"  # Replace with actual code generation
#             print(f"Verification code sent to {email}: {verification_code}")

#             # Store the code in the session for simplicity (or use database)
#             request.session['verification_code'] = verification_code

#             return JsonResponse({'message': 'Verification code sent successfully!'}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def send_verification_code(request):
    """
    Send a verification code to the user email

    If the request method is POST, get the email from the request body and send a verification code to the user email.
    If the email is not provided, return an error message.
    """

    if request.method == 'POST':
        try:
            # Parse JSON data directly from request body
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')  # Get the email from the JSON body
            print("Email:", email)
            session_code = data.get('verification_code')  # Get the verification code from the JSON body
            print("Session code:", session_code)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        verification_code = f"{random.randint(100000, 999999)}"

        user, created = CustomUser.objects.get_or_create(email=email, username=email)

        if created:
            Profile.objects.create(user=user, verification_code=verification_code, role='umuhinzi')
            # If the user is newly created, set an unusable password
            user.set_unusable_password()
            user.save()

        # Ensure the profile exists for the user
        profile, profile_created = Profile.objects.get_or_create(user=user)
        
        # Update or set the verification code
        profile.verification_code = verification_code
        profile.save()

        if session_code != verification_code:
            return JsonResponse({'error': 'Invalid verification code.'}, status=400)

        send_mail(
            _('AgriConnect Verification Code'),
            f'Your verification code is: {verification_code}',
            'rangiradave6@gmail.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Verification code sent!'}, status=200)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)
