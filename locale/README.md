# Translations Directory

This directory contains translation files for AgriConnect.

## Adding Kinyarwanda (rw) Translations

To create new translation files:

```bash
# Generate translation files
django-admin makemessages -l rw

# After translation, compile them
django-admin compilemessages -l rw
```

The translation files will be created in:
- `locale/rw/LC_MESSAGES/django.po` - Edit this file to add translations
- `locale/rw/LC_MESSAGES/django.mo` - Compiled translations (generated automatically)
```
