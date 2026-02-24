import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        # 👇 SHU YERGA QO‘SHASIZ
        print("CONNECTED USER:", user)

        if user.is_anonymous:
            print("USER IS ANONYMOUS ❌")
            await self.close()
            return

        self.group_name = f'notifications_user_{user.id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print("WEBSOCKET ACCEPTED ✅")
        await self.accept()