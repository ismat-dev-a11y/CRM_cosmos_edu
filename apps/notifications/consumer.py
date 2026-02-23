import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = f'notifications_user_{user.id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'mark_read':
            await self.mark_as_read(data['notification_id'])

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': event['notification']
        }))

    @database_sync_to_async
    def mark_as_read(self, notification_id):
        Notification.objects.filter(id=notification_id).update(is_read=True)