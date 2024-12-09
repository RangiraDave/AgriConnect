# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('signup/', views.signup, name='signup'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer-dashboard'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer-dashboard'),
    path('cooperative-dashboard/', views.cooperative_dashboard, name='cooperative-dashboard'),
    path('login/umuhinzi/', views.login_umuhinzi, name='umuhinzi_login'),
    path('login/umuguzi/', views.login_umuguzi, name='umuguzi_login'),
    path('login/cooperative/', views.login_cooperative, name='cooperative_login'),
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
]

# urlpatterns += [
#     path('dashboard/umuhinzi/', views.umuhinzi_dashboard, name='umuhinzi_dashboard'),
#     path('dashboard/umuguzi/', views.umuguzi_dashboard, name='umuguzi_dashboard'),
#     path('dashboard/cooperative/', views.cooperative_dashboard, name='cooperative_dashboard'),
# ]
