from django.urls import re_path
from django.urls import path

from .consumers import *

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/(?P<userId>)', ChatConsumer.as_asgi())
    path('ws/<str:userId>/', ChatConsumer.as_asgi())
]