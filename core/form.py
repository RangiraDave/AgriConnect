# form.py
from django.utils.translation import gettext_lazy as _

class FarmerForm(forms.Form):
    name = forms.CharField(label=_("Name"))
