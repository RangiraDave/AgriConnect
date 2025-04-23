# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from chatbot.views import chatbot_response
from django.conf import settings
from django.conf.urls.static import static
from .api_views import (
    UserViewSet, ProfileViewSet, FarmerViewSet, BuyerViewSet,
    CooperativeViewSet, ProductViewSet, ProductRatingViewSet,
    VerificationCodeViewSet
)

# router = DefaultRouter()
# router.register(r'products', ProductViewSet, basename='product')
# router.register(r'profiles', ProfileViewSet, basename='profile')
# router.register(r'ratings', ProductRatingViewSet, basename='rating')

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'buyers', BuyerViewSet, basename='buyer')
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'ratings', ProductRatingViewSet)
router.register(r'verification-codes', VerificationCodeViewSet)

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_code, name='resend_verification'),
    # path('farmers/', views.farmer_list, name='farmer_list'),
    path('products/', views.product_listings, name='product_listings'),
    path('add-product/', views.add_product, name='add_product'),
    path('profile/', views.user_profile, name='user_profile'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/rate/', views.rate_product, name='rate_product'),
    path('chatbot/get_response/', chatbot_response, name='chatbot_response'),
    path('market-insights/', views.market_insights, name='market_insights'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('api/', include(router.urls)),  # Add API routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
