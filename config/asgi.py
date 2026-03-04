import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import apps.notifications.routing

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token['user_id']
        from apps.users.models import UserProfile
        return UserProfile.objects.get(id=user_id)
    except Exception as e:
        print("JWT ERROR:", e)
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = None

        # 1. Header dan olish (wscat uchun)
        if b'authorization' in headers:
            auth = headers[b'authorization'].decode()
            if auth.startswith('Bearer '):
                token = auth.split(' ')[1]

        # 2. Query param dan olish (brauzer/HTML uchun)
        if not token:
            query_string = scope.get('query_string', b'').decode()
            for param in query_string.split('&'):
                if param.startswith('token='):
                    token = param.split('=')[1]
                    break

        scope['user'] = await get_user(token) if token else AnonymousUser()
        return await self.app(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            apps.notifications.routing.websocket_urlpatterns
        )
    ),
})