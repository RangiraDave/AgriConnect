# core/urls.py
from django.urls import path
from . import views
from chatbot.views import chatbot_response  # Import the chatbot view
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
