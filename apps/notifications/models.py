from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'Xabar'),
        ('grade', 'Baho'),
        ('attendance', 'Davomat'),
        ('announcement', 'Elon'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']