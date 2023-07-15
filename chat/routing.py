from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('real_time_chat/', consumers.ChatConsumer.as_asgi()),
]