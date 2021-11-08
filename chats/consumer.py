import asyncio
import json


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


from chats.models import Chat, Message
from chats.serializers import MessageSerializer


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):

       self.room_name = self.scope['url_route']['kwargs']['chat_link']
       self.room_group_name = f'chat_{self.room_name}'

       self.chat = await self.get_chat(self.room_name)

       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )

       await self.accept()

    async def send_recently(self, message_json):
       message_text = message_json.get('text', '')
       is_anonymous = message_json.get('is_anonymous', False)
       new_message = await self.create_message(chat=self.chat, author=self.scope['user'],
                                                message_text=message_text, is_anonymous=is_anonymous)
       response_data = MessageSerializer(new_message).data
       await self.channel_layer.group_send(
            self.room_group_name,
            {
                'message': response_data,
                'type': 'chat_message',
                'sender_id': self.scope['user'].id
            }
        )

    async def send_with_delay(self, delay, message_json):
        await asyncio.sleep(delay)
        await self.send_recently(message_json=message_json)

    async def receive(self, text_data):
        message_json = json.loads(text_data)
        send_after = message_json.get('send_after', 0)

        if send_after > 0:
            asyncio.create_task(self.send_with_delay(delay=send_after, message_json=message_json))
        else:
            await self.send_recently(message_json=message_json)

    async def chat_message(self, event):

        if event['message']['author']['username'] == 'AnonymousUser':
            if event['sender_id'] == self.scope['user'].id:
                event['message']['author'].update({"its_me": True})
            else:
                event['message']['author'].update({"its_me": False})

        await self.send(
                text_data=json.dumps({
                    'message': event['message']
                })
        )

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_message(self, chat, author, message_text, is_anonymous):
        try:
            author = author
            new_message = Message.objects.create(chat=chat, author=author, text=message_text, is_anonymous=is_anonymous)

            return new_message
        except Exception as e:
            print(e)

    @database_sync_to_async
    def get_chat(self, chat_link):
        return Chat.objects.get(short_link=chat_link)