# core/urls.py
from django.urls import path
from . import views
from chatbot.views import chatbot_response
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_code, name='resend_verification'),
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('products/', views.product_listings, name='product_listings'),
    path('add-product/', views.add_product, name='add_product'),
    path('profile/', views.user_profile, name='user_profile'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/rate/', views.rate_product, name='rate_product'),
    path('chatbot/get_response/', chatbot_response, name='chatbot_response'),
    path('market-insights/', views.market_insights, name='market_insights'),
    path('delete-account/', views.delete_account, name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
