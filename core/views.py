from django.shortcuts import render
from django.utils.translation import gettext as _

welcome_message = _("Welcome to AgriConnect!")

def homepage(request):
    return render(request, 'core/home.html')
