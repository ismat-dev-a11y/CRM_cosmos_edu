from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(sender, recipient, title, message, notif_type='message'):
    """Istalgan joydan chaqirish mumkin"""

    # DB ga saqlash
    notif = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notif_type
    )

    # WebSocket orqali yuborish
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_user_{recipient.id}',
        {
            'type': 'send_notification',
            'notification': {
                'id': notif.id,
                'title': title,
                'message': message,
                'type': notif_type,
            }
        }
    )
    return notif