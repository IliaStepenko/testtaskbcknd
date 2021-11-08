from django.urls import path
from rest_framework.routers import DefaultRouter

from chats.viewsets import ChatViewSet

router = DefaultRouter()

router.register('chat', ChatViewSet, basename='chat')

urlpatterns = router.urls