from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('get_response/', views.chatbot_response, name='get_response'),
]
