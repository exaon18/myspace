import os
from django.core.asgi import get_asgi_application

# 1. Set the settings module environment variable first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myspace.settings')

# 2. Initialize Django ASGI application early to populate the AppRegistry.
# This MUST happen before importing any consumers, models, or local middleware.
django_asgi_app = get_asgi_application()

# 3. NOW it is safe to import Channels routing, consumers, and middleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from core.consumers import CampfireConsumer
# Safe to import now

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    
    "websocket": 
        # 4. Wrap your router with your custom Telegram auth middleware 
        # (You can nest it inside AuthMiddlewareStack if you still need standard session/user handling)
        AuthMiddlewareStack(
            URLRouter([
                # Matches the frontend ws:// protocols pointing to /ws/campfire/
                path("wss/campfire/", CampfireConsumer.as_asgi()),
            ]))
        
    ,
})