from rest_framework import serializers

from chats.models import Chat, Message
from users.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        lookup_field = 'short_link'
        fields = ('name', 'short_link')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'author', 'text', 'send_date')

    author = serializers.SerializerMethodField()
    send_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_author(self, data):

        if data.is_anonymous:
            user = self.context.get('user', None)

            if user is None:
                request = self.context.get('request', None)
                user = request.user if hasattr(request, 'user') else None

            if user is not None and (user == data.author or user.is_superuser):
                serialized_data = UserSerializer(data.author).data
                serialized_data.update({'is_anonymous': True})
                return serialized_data
            else:
                return {field: 'AnonymousUser' for field in UserSerializer.Meta.fields}

        else:
            return UserSerializer(data.author).data



