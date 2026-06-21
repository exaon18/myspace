import urllib.parse
import hmac
import hashlib
import json
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
from .models import Myuser

@database_sync_to_async
def get_user_from_telegram(init_data_string):
    # 1. Parse and validate
    parsed_data = urllib.parse.parse_qs(init_data_string)
    if 'hash' not in parsed_data: return AnonymousUser()
    
    received_hash = parsed_data.pop('hash')[0]
    data_check_string = "\n".join([f"{k}={v[0]}" for k in sorted(parsed_data.keys())])
    
    secret_key = hmac.new("WebAppData".encode(), settings.TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if hmac.compare_digest(calculated_hash, received_hash):
        user_data = json.loads(parsed_data['user'][0])
        user, _ = Myuser.objects.get_or_create(tgID=user_data.get('id'), defaults={'username': user_data.get('username')})
        return user
    return AnonymousUser()

# middleware.py
import urllib.parse
# ... keep your imports ...

class TelegramAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_data = urllib.parse.parse_qs(query_string)
        init_data = query_data.get("initData", [None])[0]

        print(f"DEBUG: Middleware received initData: {init_data is not None}")
        
        if init_data:
            user = await get_user_from_telegram(init_data)
            scope["user"] = user
            print(f"DEBUG: Middleware assigned user: {user.username if user else 'None'}")
        else:
            print("DEBUG: Middleware found NO initData, setting AnonymousUser")
            scope["user"] = AnonymousUser()
            
        return await self.inner(scope, receive, send)