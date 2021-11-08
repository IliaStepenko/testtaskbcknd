from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.consumer import ChatRoomConsumer

websockets_urlpatterns = [
    path(
        "ws/chats/chat/<str:chat_link>/", ChatRoomConsumer.as_asgi(), name="chat",
    ),
]