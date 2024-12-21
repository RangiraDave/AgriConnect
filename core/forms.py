# form.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Product


class FarmerForm(forms.Form):
    name = forms.CharField(label=_("Name"))


class AddProductForm(forms.ModelForm):
    """ Form to add a product """
    class Meta:
        model = Product
        fields = ['name', 'description', 'media', 'price_per_unit', 'quantity_available']
		
    def clean_quantity_available(self):
        quantity = self.cleaned_data['quantity_available']

        if not isinstance(quantity, int) or quantity < 0:
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
