from django.urls import re_path
from .consumers import RatingNotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/notifications/$', RatingNotificationConsumer.as_asgi()),
]
