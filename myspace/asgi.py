# your_project_name/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from core.consumers import CampfireConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myspace.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Matches the frontend ws:// protocols pointing to /ws/campfire/
            path("ws/campfire/", CampfireConsumer.as_asgi()),
        ])
    ),
})