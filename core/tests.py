# tests.py
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile, Farmer, Product, VerificationCode
from django.core import mail
import uuid

User = get_user_model()

class CoreViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        # Create a test user for login and profile testing
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '123456Test!',
            'role': 'umuhinzi'
        }
        self.user = User.objects.create_user(**self.user_data)
        Profile.objects.create(user=self.user, phone="07888888", role='umuhinzi')
        
        # Log in the test user for subsequent tests that require authentication 
        self.client.login(username=self.user_data['email'], password=self.user_data['password'])

    def test_homepage_view(self):
        """ Test if homepage renders correctly """
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_farmer_list_view(self):
        """ Test if farmer list view renders correctly """
        response = self.client.get(reverse('farmer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/farmer_list.html')

    def test_login_view(self):
        """ Test if login view redirects authenticated users to product listings """
        response = self.client.post(reverse('login'), data={
            **self.user_data,
            "role": "umuhinzi",
        })
        # Since the user is already logged in by default in setup(), this should redirect directly to profile or product listings.
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_signup_and_verification_flow(self):
        """ Test signup and email verification flow """
        
        # Sign up a new user
        signup_response = self.client.post(reverse('signup'), data={
            **self.user_data,
            "phone": "1234567",
            "confirm_password": "123456Test!",
            "role": "umuhinzi"
        })
        
        # Check if we are redirected to verify email page after signup.
        self.assertEqual(signup_response.status_code, 200)
        
        # Check if an email was sent
        self.assertGreater(len(mail.outbox), 0, "No email was sent during signup.")
        
        # Get the last sent email (verification code)
        verification_email = mail.outbox[-1]
        
        # Verify the email content contains a verification code 
        verification_code_from_email = verification_email.body.split()[-1]
        
        # Verify with the correct code 
        verify_response = self.client.post(reverse('verify_email'), data={'verification_code': verification_code_from_email})
        
        # Check redirection to login page upon successful verification 
        self.assertEqual(verify_response.url, reverse('login'))

    def test_product_listings_view(self):
        """ Test if product listing view renders correctly """
        
        Product.objects.create(owner=self.user, name="Test Product", price_per_unit=10.99)
        
        response = self.client.get(reverse('product_listings'))
        
        # Assertions:
        self.assertEqual(response.status_code, 200, 'Product listing page did not load')
        self.assertTemplateUsed(response, 'core/product_listings.html')
        self.assertIn('products', response.context)

    def test_add_product_view(self):
        """ Creating New Product """
        
        # Use form data to simulate POST request to `/add-product/`
        form_data = {
            "name": "New Test Product",
            "description": "A new product for testing purposes.",
            # "media": ...,   ## Assuming you have a file upload method here. Remove comments or adjust accordingly.
            "price_per_unit": "15.99",
            "quantity_available": "5"
        }
        
        add_product_response = self.client.post(reverse('add_product'), form_data)
        
        # Assertions:
        self.assertEqual(add_product_response.status_code, 302, "Adding new product didn't result in redirection.")
        self.assertGreater(len(Product.objects.filter(name="New Test Product")), 0, "Product wasn't created successfully.")

if __name__ == '__main__':
    unittest.main()
