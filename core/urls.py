# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('signup/', views.signup, name='signup'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer-dashboard'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer-dashboard'),
    path('cooperative-dashboard/', views.cooperative_dashboard, name='cooperative-dashboard'),
    path('login/', views.login_view, name='login'),
    # 
    path(
        'verify-email/',
        views.verify_email,
        name='verify_email'
    ),
    path(
        'resend-code/',
        views.resend_verification_code,
        name='resend_code'
    ),
    path('products/', views.product_listings, name='product_listings'),
    path('add-product/', views.add_product, name='add_product'),
]
