from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from core.views import debug_db_config
from django.conf.urls.i18n import i18n_patterns

# Non-translatable URLs
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching URL
]

# Translatable URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/', include('core.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('debug/db-config/', debug_db_config, name='debug_db_config'),
    prefix_default_language=True,  # Always prefix URLs with language code
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
