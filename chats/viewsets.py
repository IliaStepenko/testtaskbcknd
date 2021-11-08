from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from chats.models import Message, Chat
from chats.serializers import ChatSerializer, MessageSerializer


class ChatViewSet(ModelViewSet):
    model = Chat
    lookup_field = 'short_link'
    queryset = model.objects.all()
    serializer_class = ChatSerializer

    def get_serializer_class(self):
        if self.action == 'messages':
            return MessageSerializer
        else:
            return ChatSerializer

    @action(detail=True, methods=['get'])
    def messages(self, request, short_link=None):

        if short_link is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(chat__short_link=short_link).order_by("send_date")

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, context={'request': self.request}, many=True)
            return self.get_paginated_response(serializer.data)


