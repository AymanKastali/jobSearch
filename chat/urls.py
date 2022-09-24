from django.urls import path
from .views import *

urlpatterns = [
    path('<str:userId>/', chat, name='chat-id'),
]