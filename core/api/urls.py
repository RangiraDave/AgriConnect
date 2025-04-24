from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    signup, verify_email, login,
    profile, ProductViewSet, market_insights
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/verify/', verify_email),
    path('auth/login/', login),
    path('profile/', profile),
    path('market-insights/', market_insights),
    path('', include(router.urls)),
]
