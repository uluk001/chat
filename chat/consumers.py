from .models import CustomUser, Chat, Message
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.chat = await self.get_chat()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.set_online()
        await self.get_messages()

    async def disconnect(self, close_code):
        await self.set_offline()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.save_message(data)
        data['sender'] = self.user.username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    async def chat_message(self, event):
        if event['data']['sender'] == self.user.username:
            return
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def get_chat(self):
        chat = await sync_to_async(Chat.objects.get, thread_sensitive=True)(id=self.chat_id)
        return chat

    async def set_online(self):
        self.user.is_online = True
        await sync_to_async(self.user.save, thread_sensitive=True)()

    async def set_offline(self):
        self.user.is_online = False
        await sync_to_async(self.user.save, thread_sensitive=True)()

    async def get_messages(self):
        # Загружаем сообщения и связанные объекты sender
        messages_with_sender = await sync_to_async(
            list, thread_sensitive=True
        )(
            Message.objects.select_related('sender').filter(chat=self.chat)
        )

        for message in messages_with_sender:
            data = {
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': str(message.timestamp),
                'media_file': str(message.media_file),
                'is_deleted': message.is_deleted,
                'edited_at': str(message.edited_at) if message.edited_at else ''
            }
            await self.send(text_data=json.dumps(data))

    async def save_message(self, data):
        # Предполагается, что 'media_file' в data - это путь к файлу или URL
        # Если это не так, вам потребуется дополнительная логика для обработки 'media_file'
        message = await sync_to_async(Message.objects.create, thread_sensitive=True)(
            chat=self.chat,
            sender=self.user,
            content=data['content'],
            media_file=data.get('media_file', '')
        )
        # Этот вызов может потребовать дополнительной логики, в зависимости от того, как вы используете 'group_send'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': {
                    'sender': self.user.username,
                    'content': message.content,
                    'timestamp': str(message.timestamp),
                    'media_file': str(message.media_file),
                    'is_deleted': message.is_deleted,
                    'edited_at': str(message.edited_at)
                }
            }
        )
