# core/forms.py

from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Product, Profile, Province, District, Sector, Cell, Village, Farmer, Cooperative
from django.contrib.auth import get_user_model
import os
from captcha.fields import CaptchaField

User = get_user_model()

class FarmerForm(forms.Form):
    name = forms.CharField(label=_("Name"))


class AddProductForm(forms.ModelForm):
    """
    Form for adding a new product, now including hidden latitude/longitude fields.
    """
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'media',
            'price_per_unit',
            'quantity_available',
            'unit',
            'contact',
            'latitude',
            'longitude',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter product description'
            }),
            'media': forms.FileInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter price per unit'
            }),
            'quantity_available': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter available quantity'
            }),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter contact number (optional)'
            }),
            # latitude/longitude use HiddenInput, so no need to define here
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set autocomplete attributes for all fields
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['autocomplete'] = 'off'
        self.fields['price_per_unit'].widget.attrs['autocomplete'] = 'off'
        self.fields['quantity_available'].widget.attrs['autocomplete'] = 'off'
        self.fields['unit'].widget.attrs['autocomplete'] = 'off'
        self.fields['contact'].widget.attrs['autocomplete'] = 'tel'
        self.fields['latitude'].widget.attrs['autocomplete'] = 'off'
        self.fields['longitude'].widget.attrs['autocomplete'] = 'off'

    def clean(self):
        cleaned_data = super().clean()
        media = cleaned_data.get('media')

        if media:
            # Enforce 5MB limit
            if media.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("File size must be no more than 5MB."))

            # Only allow .jpg, .jpeg, .png, .mp4
            ext = os.path.splitext(media.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.mp4']:
                raise forms.ValidationError(_("Only JPG, PNG, and MP4 files are allowed."))

        return cleaned_data

    def save(self, commit=True):
        """
        Override save() in case you need to do something special with latitude/longitude.
        By default, ModelForm.save() will automatically assign cleaned_data['latitude']
        to product.latitude, and similarly for longitude.
        """
        product = super().save(commit=False)
        # Example: you could default missing lat/lng here if you want.
        # lat = self.cleaned_data.get('latitude')
        # lng = self.cleaned_data.get('longitude')
        # if lat and lng:
        #     product.latitude = lat
        #     product.longitude = lng

        if commit:
            product.save()
        return product


class EditProductForm(forms.ModelForm):
    """
    Form to edit an existing product. Also includes hidden latitude/longitude
    in case you want to allow editing those later (optional).
    """
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'media',
            'price_per_unit',
            'quantity_available',
            'unit',
            'contact',
            'latitude',
            'longitude',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter product description'
            }),
            'media': forms.FileInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter price per unit'
            }),
            'quantity_available': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter available quantity'
            }),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter contact number (optional)'
            }),
            # latitude/longitude use HiddenInput
        }

    def clean(self):
        cleaned_data = super().clean()
        media = cleaned_data.get('media')

        if media:
            # Enforce 5MB limit
            if media.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("File size must be no more than 5MB."))

            # Only allow .jpg, .jpeg, .png, .mp4
            ext = os.path.splitext(media.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.mp4']:
                raise forms.ValidationError(_("Only JPG, PNG, and MP4 files are allowed."))

        return cleaned_data

    def clean_quantity_available(self):
        quantity = self.cleaned_data.get('quantity_available')
        if quantity is None or quantity < 0:
            raise forms.ValidationError(_("Quantity must be a non-negative number."))
        return quantity


class SignupForm(forms.Form):
    """
    Form to handle user signup with email/phone/role validation.
    """
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('The username is already taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('The email is already in use.'))
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('The phone number is already in use.'))
        return phone

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_('Passwords do not match.'))
        return confirm_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
        if len(password) < 6:
            errors.append(_('Password must be at least 6 characters long.'))
        if not any(c.isupper() for c in password):
            errors.append(_('Password must contain at least one uppercase letter.'))
        if not any(c.islower() for c in password):
            errors.append(_('Password must contain at least one lowercase letter.'))
        if not any(c.isdigit() for c in password):
            errors.append(_('Password must contain at least one digit.'))
        if errors:
            raise forms.ValidationError(errors)
        return password


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile (username, name, phone, avatar, bio, location).
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Full Name')
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label=_('Profile Picture')
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label=_('Bio')
    )
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Province')
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('District')
    )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Sector')
    )
    cell = forms.ModelChoiceField(
        queryset=Cell.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Cell')
    )
    village = forms.ModelChoiceField(
        queryset=Village.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Village')
    )
    specific_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Specific Location')
    )
    role = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label=_('Role')
    )

    class Meta:
        model = Profile
        fields = [
            'username',
            'name',
            'phone',
            'role',
            'avatar',
            'bio',
        ]
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['name'].initial = self.instance.name
        self.fields['phone'].initial = self.instance.phone
        self.fields['bio'].initial = self.instance.bio
        self.fields['role'].initial = self.instance.role

        # Pre-fill location if the profile has an associated Farmer or Cooperative
        location = getattr(self.instance, 'farmer', None) or getattr(self.instance, 'cooperative', None)
        province_id = None
        district_id = None
        sector_id = None
        cell_id = None
        village_id = None
        specific_location = None

        if self.is_bound:
            province_id = self.data.get('province') or None
            district_id = self.data.get('district') or None
            sector_id = self.data.get('sector') or None
            cell_id = self.data.get('cell') or None
            village_id = self.data.get('village') or None
            specific_location = self.data.get('specific_location') or None
        elif location:
            province_id = location.province_id
            district_id = location.district_id
            sector_id = location.sector_id
            cell_id = location.cell_id
            village_id = location.village_id
            specific_location = location.specific_location
            self.fields['province'].initial = province_id
            self.fields['district'].initial = district_id
            self.fields['sector'].initial = sector_id
            self.fields['cell'].initial = cell_id
            self.fields['village'].initial = village_id
            self.fields['specific_location'].initial = specific_location

        # Restrict child dropdowns to their parent selection
        self.fields['district'].queryset = \
            District.objects.filter(province_id=province_id) if province_id else District.objects.none()
        self.fields['sector'].queryset = \
            Sector.objects.filter(district_id=district_id) if district_id else Sector.objects.none()
        self.fields['cell'].queryset = \
            Cell.objects.filter(sector_id=sector_id) if sector_id else Cell.objects.none()
        self.fields['village'].queryset = \
            Village.objects.filter(cell_id=cell_id) if cell_id else Village.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        province = cleaned_data.get('province')
        district = cleaned_data.get('district')
        sector = cleaned_data.get('sector')
        cell = cleaned_data.get('cell')
        village = cleaned_data.get('village')
        any_location = any([province, district, sector, cell, village])

        if any_location:
            # If any is filled, then all must be filled
            if not all([province, district, sector, cell, village]):
                raise forms.ValidationError(
                    _('If you provide location, all location fields are required.')
                )
            # Validate parent‐child relationships
            if district and district.province != province:
                raise forms.ValidationError(_('Selected district does not belong to the selected province.'))
            if sector and sector.district != district:
                raise forms.ValidationError(_('Selected sector does not belong to the selected district.'))
            if cell and cell.sector != sector:
                raise forms.ValidationError(_('Selected cell does not belong to the selected sector.'))
            if village and village.cell != cell:
                raise forms.ValidationError(_('Selected village does not belong to the selected cell.'))

        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        profile.name = self.cleaned_data.get('name', '')
        user.save()

        if commit:
            profile.save()

            province = self.cleaned_data.get('province')
            district = self.cleaned_data.get('district')
            sector = self.cleaned_data.get('sector')
            cell = self.cleaned_data.get('cell')
            village = self.cleaned_data.get('village')
            specific_location = self.cleaned_data.get('specific_location')

            if any([province, district, sector, cell, village, specific_location]):
                location = getattr(profile, 'farmer', None) or getattr(profile, 'cooperative', None)
                if location:
                    location.province = province
                    location.district = district
                    location.sector = sector
                    location.cell = cell
                    location.village = village
                    location.specific_location = specific_location
                    location.save()
                else:
                    # If no Farmer/Cooperative object yet, create one
                    Farmer.objects.create(
                        profile=profile,
                        province=province,
                        district=district,
                        sector=sector,
                        cell=cell,
                        village=village,
                        specific_location=specific_location
                    )
        return profile


class LoginForm(forms.Form):
    """
    Simple login form with email, password, role, and a captcha field.
    """
    email = forms.EmailField(
        label=_('Email Address'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Enter your email')
        })
    )
    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Enter your password')
        })
    )
    role = forms.ChoiceField(
        label=_('Role'),
        choices=Profile.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    recaptcha = CaptchaField(label=_('Captcha'))

