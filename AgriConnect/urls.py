from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import debug_db_config
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.views.static import serve
import os

# Non-translatable URLs
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching URL
    path('i18n/setlang/', set_language, name='set_language'),
]

# Serve media files in development
if settings.DEBUG:
    # Serve media files through Django in development
    urlpatterns = [
        # Add media URL pattern before i18n_patterns
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ] + urlpatterns
    
    # Serve static files
    urlpatterns += staticfiles_urlpatterns()
else:
    # In production, serve media files through the web server (Nginx/Apache)
    # This is a fallback and should be handled by the web server in production
    urlpatterns = [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ] + urlpatterns
    
    # Serve static files in production
    urlpatterns += staticfiles_urlpatterns()

# Translatable URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/', include('core.api.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/locations/', include('core.api_urls')),  # Add location API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('debug/db-config/', debug_db_config, name='debug_db_config'),
    path('chatbot/', include('chatbot.urls')),  # Include chatbot URLs
    prefix_default_language=True,  # Always prefix URLs with language code
)
