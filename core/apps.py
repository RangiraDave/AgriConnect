# core/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import _trans


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Register custom languages

        # Register Kinyarwanda language if it doesn't exist
        if 'rw' not in _trans.LANG_INFO:
            _trans.LANG_INFO['rw'] = {
                'bidi': False,  # Right-to-left or not
                'code': 'rw',
                'name': 'Kinyarwanda',
                'name_local': 'Ikinyarwanda',
            }