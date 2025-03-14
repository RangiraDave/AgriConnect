# core/urls.py
from django.urls import path
from . import views
from chatbot.views import chatbot_response  # Import the chatbot view from the correct module
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('signup/', views.signup, name='signup'),
    path('cooperative-dashboard/', views.cooperative_dashboard, name='cooperative-dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-code/', views.resend_verification_code, name='resend_code'),
    path('products/', views.product_listings, name='product_listings'),
    path('add-product/', views.add_product, name='add_product'),
    path('profile/', views.user_profile, name='user_profile'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('chatbot/get_response/', chatbot_response, name='chatbot_response'),  # Add chatbot response URL
    path('delete-account/', views.delete_account, name='delete_account'),  # Ensure this URL pattern is defined
    path('rate_product/<int:product_id>/', views.ajax_rate_product, name='ajax_rate_product'),  # Ensure this URL pattern is defined
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('rate-product/<int:product_id>/', views.rate_product, name='rate_product'),
    path('market-insights/', views.market_insights, name='market_insights'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
