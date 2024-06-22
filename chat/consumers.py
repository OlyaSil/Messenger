import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, GroupChat
from django.contrib.auth.models import User
from django.utils import timezone
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # Save message to database
        group = await sync_to_async(GroupChat.objects.get)(name=self.room_name)
        msg = await sync_to_async(Message.objects.create)(
            group=group,
            sender=user,
            content=message,
            timestamp=timezone.now()
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'email': user.email,  # Use user's email for identification
                'timestamp': msg.timestamp.isoformat()  # send the timestamp of the message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        email = event['email']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'email': email,  # include user's email in the message
            'timestamp': timestamp,  # include timestamp in the message
        }))