# core/urls.py
from django.urls import path
from . import views
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

    # Chat URLs
    path('chat/list/', views.chat_list, name='chat_list'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('chat/<str:room_name>/send/', views.send_message, name='send_message'),
    path('chat/start/<int:product_id>/<int:user_id>/', views.start_private_chat, name='start_private_chat'),
    path('chat/private/<int:conversation_id>/', views.private_chat, name='private_chat'),

    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/send/<int:user_id>/<str:message>/', views.send_notification, name='send_notification'),
    #
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
