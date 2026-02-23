# views.py da o'qituvchi ota-onaga xabar yuboradi
from notifications.signals import send_notification
from apps.users.models import UserProfile

def teacher_send_message(request):
    parent = UserProfile.objects.get(id=request.data['parent_id'])

    send_notification(
        sender=request.user,        # O'qituvchi
        recipient=parent,           # Ota-ona
        title="Dars haqida",
        message="Farzandingiz bugun darsda faol qatnashdi!",
        notif_type='message'
    )