import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from decouple import config  # For reading environment variables
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Should be before django.contrib.admin
    'captcha',  # django-recaptcha
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'core',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'widget_tweaks',  # for form rendering
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AgriConnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AgriConnect.wsgi.application'

# Channels configuration
ASGI_APPLICATION = 'AgriConnect.routing.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
logger = logging.getLogger(__name__)

try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': 60,  # Keep connections alive for 60 seconds
            'OPTIONS': {
                'connect_timeout': 10,  # Connection timeout in seconds
            }
        }
    }
    logger.info(f"Database configuration loaded successfully. Host: {config('DB_HOST', default='localhost')}")
except Exception as e:
    logger.error(f"Error loading database configuration: {str(e)}")
    raise

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = [
    ('en', _('English')),
    ('rw', _('Kinyarwanda')),
]

LANGUAGE_CODE = 'rw'  # Default language
TIME_ZONE = 'Africa/Kigali'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Session settings for language preference
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Media file settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Ensure media directory exists
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
    os.makedirs(os.path.join(MEDIA_ROOT, 'products'))

# Add whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'core.CustomUser'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'core.auth_backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'EXCEPTION_HANDLER': 'core.api.api_views.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


# Enable CORS for all origins (adjust as needed for production)
CORS_ALLOW_ALL_ORIGINS = True

# Channels layers configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

LOGIN_URL = '/login/'

# Jazzmin UI Customizations (Optional, but recommended for a "cool" look)
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "AgriConnect Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "AgriConnect",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "AgriConnect",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to AgriConnect Admin",

    # Copyright on the footer
    "copyright": "AgriConnect Ltd",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": 'profile.avatar',

    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["core.view_customuser"]},
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "core.CustomUser"},
        {"app": "core"},
    ],

    #############
    # User Menu #
    #############
    "usermenu_links": [
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "core.CustomUser"}
    ],

    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "core", "core.Product", "core.UserProfile"],

    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "core.CustomUser": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Product": "fas fa-shopping-basket",
        "core.UserProfile": "fas fa-id-card",
        "core.Order": "fas fa-file-invoice-dollar",
        "core.Category": "fas fa-tags",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "core.CustomUser": "collapsible",
        "auth.Group": "vertical_tabs"
    },
    "language_chooser": False,  # Change to True once translations are properly set up
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success", # "navbar-indigo", "navbar-purple", etc.
    "accent": "accent-success", # "accent-primary", "accent-warning", etc.
    "navbar": "navbar-success navbar-dark", # "navbar-white navbar-light", "navbar-dark"
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success", # "sidebar-dark-primary", "sidebar-light-primary"
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default", # "cerulean", "cosmo", "cyborg", "darkly", "flatly", "journal", "litera", "lumen", "lux", "materia", "minty", "pulse", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab", "superhero", "united", "yeti"
    "dark_mode_theme": "darkly", # Optional: A theme to use for dark mode
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# reCAPTCHA v3 settings (add your keys to .env)
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_DEFAULT_ACTION = 'login'
RECAPTCHA_SCORE_THRESHOLD = 0.5
