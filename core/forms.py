# form.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Product
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class FarmerForm(forms.Form):
    name = forms.CharField(label=_("Name"))


class AddProductForm(forms.ModelForm):
    """ Form to add a product """
    class Meta:
        model = Product
        fields = ['name', 'description', 'contact', 'media', 'price_per_unit', 'quantity_available']

    def clean_quantity_available(self):
        quantity = self.cleaned_data['quantity_available']
        if quantity < 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity


class EditProductForm(forms.ModelForm):
    """ Form to edit a product """
    class Meta:
        model = Product
        fields = ['name', 'description', 'media', 'price_per_unit', 'quantity_available']

    def clean_quantity_available(self):
        quantity = self.cleaned_data['quantity_available']

        if not isinstance(quantity, int) or quantity < 0:
            raise forms.ValidationError("Quantity must be a positive number.")

        return quantity


class SignupForm(forms.Form):
    """
    SignupForm to handle the validation
    """
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    def clean_username(self):
        """
        Check if the username is unique
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username is already taken.')
        return username

    def clean_email(self):
        """
        Check if the email is unique
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email is already in use.')
        return email

    def clean_phone(self):
        """
        Check if the phone number is unique
        """
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('The phone number is already in use.')
        return phone

    def clean_confirm_password(self):
        """
        Check if the passwords match
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return confirm_password
