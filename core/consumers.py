import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RatingNotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None  # Initialize group_name to avoid AttributeError

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.scope['user'].id}"  # Set group_name
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if self.group_name:  # Ensure group_name is not None before using it
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def rating_notification(self, event):
        message = event.get("message", "")
        await self.send(text_data=json.dumps({"message": message}))
