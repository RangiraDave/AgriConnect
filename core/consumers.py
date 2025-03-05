# core/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles WebSocket connections for the chat room.
    """
    async def connect(self):
        """
        Called when the websocket is handshaking as part of the connection process.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        """
        Called when the consumer receives data from the WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Save message to database
        await self.save_message(message, user)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        """
        Called when the consumer receives a message from the room group.
        """
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @sync_to_async
    def save_message(self, message, user):
        """
        Save a message to the database.
        """
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=user, content=message)


class RatingNotificationConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles WebSocket connections for rating notifications.
    """
    async def connect(self):
        self.user_group = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def rating_notification(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
