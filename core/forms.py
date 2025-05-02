# form.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Product
from django.contrib.auth import get_user_model
from .models import Profile
from .models import Province, District, Sector, Cell, Village, Farmer, Cooperative

User = get_user_model()

class FarmerForm(forms.Form):
    name = forms.CharField(label=_("Name"))


class AddProductForm(forms.ModelForm):
    """ Form to add a product """
    class Meta:
        model = Product
        fields = ['name', 'contact', 'description', 'media', 'price_per_unit', 'quantity_available', 'unit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'media': forms.FileInput(attrs={'accept': 'image/*,video/mp4'}),
        }

    def clean_quantity_available(self):
        quantity = self.cleaned_data['quantity_available']
        if quantity < 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity


class EditProductForm(forms.ModelForm):
    """ Form to edit a product """
    class Meta:
        model = Product
        fields = ['name', 'contact', 'description', 'media', 'price_per_unit', 'quantity_available', 'unit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'media': forms.FileInput(attrs={'accept': 'image/*,video/mp4'}),
        }

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


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile."""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = ['username', 'phone', 'role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        
        # Add location fields if user is farmer or cooperative
        if self.instance.role in ['umuhinzi', 'cooperative']:
            try:
                if self.instance.role == 'umuhinzi':
                    location = self.instance.farmer
                else:
                    location = self.instance.cooperative
            except (Farmer.DoesNotExist, Cooperative.DoesNotExist):
                location = None
            
            # Province field
            self.fields['province'] = forms.ModelChoiceField(
                queryset=Province.objects.all(),
                initial=location.province_id if location and location.province else None,
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
            # District field
            self.fields['district'] = forms.ModelChoiceField(
                queryset=District.objects.filter(province=location.province) if location and location.province else District.objects.none(),
                initial=location.district_id if location and location.district else None,
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
            # Sector field
            self.fields['sector'] = forms.ModelChoiceField(
                queryset=Sector.objects.filter(district=location.district) if location and location.district else Sector.objects.none(),
                initial=location.sector_id if location and location.sector else None,
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
            # Cell field
            self.fields['cell'] = forms.ModelChoiceField(
                queryset=Cell.objects.filter(sector=location.sector) if location and location.sector else Cell.objects.none(),
                initial=location.cell_id if location and location.cell else None,
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
            # Village field
            self.fields['village'] = forms.ModelChoiceField(
                queryset=Village.objects.filter(cell=location.cell) if location and location.cell else Village.objects.none(),
                initial=location.village_id if location and location.village else None,
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
            # Specific location field
            self.fields['specific_location'] = forms.CharField(
                max_length=255,
                required=False,
                initial=location.specific_location if location else '',
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    
    def clean(self):
        cleaned_data = super().clean()
        role = self.instance.role
        
        # Validate required fields for farmers and cooperatives
        if role in ['umuhinzi', 'cooperative']:
            required_fields = ['province', 'district', 'sector', 'cell', 'village']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, _('This field is required for farmers and cooperatives.'))
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(_('This phone number is already registered.'))
        return phone
