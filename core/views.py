import json
import urllib.parse
import hmac
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.conf import settings
from .models import Myuser

import urllib.parse
import hmac
import hashlib
import json

def verify_telegram_web_app(init_data_string, bot_token):
    # 1. Parse the query string
    # parse_qs returns: {'user': ['{...}'], 'auth_date': ['12345'], 'hash': ['abc...']}
    parsed_data = urllib.parse.parse_qs(init_data_string)
    
    if 'hash' not in parsed_data:
        return None
    
    # 2. Extract the hash and remove it for the data_check_string
    received_hash = parsed_data.pop('hash')[0]
    
    # 3. Correctly sort and join the data
    # We must join the first element of each list (v[0])
    data_check_list = []
    for key in sorted(parsed_data.keys()):
        data_check_list.append(f"{key}={parsed_data[key][0]}")
    
    data_check_string = "\n".join(data_check_list)
    
    # 4. Generate the secret key (HMAC-SHA256 of "WebAppData" with bot token)
    secret_key = hmac.new(
        "WebAppData".encode(), 
        bot_token.encode(), 
        hashlib.sha256
    ).digest()
    
    # 5. Generate the hash
    calculated_hash = hmac.new(
        secret_key, 
        data_check_string.encode(), 
        hashlib.sha256
    ).hexdigest()
    print("Calculated Hash:", calculated_hash, "Received Hash:", received_hash)
    # 6. Compare hashes
    if hmac.compare_digest(calculated_hash, received_hash):
        # Successfully validated! Now safely parse the user JSON
        print(json.loads(parsed_data['user'][0]))
        return json.loads(parsed_data['user'][0])
    
    return None

@csrf_exempt
def home(request):
    if request.method == 'POST':
        # Expect the raw initData string from the frontend
        body = json.loads(request.body)
        init_data_string = body.get('initData')
        # Validate data against your BOT_TOKEN from settings
        user_data = verify_telegram_web_app(init_data_string, "8931595168:AAHSAaKz6ld4OKtb-fkS2C-raUlyevQ_zt8")
        if not user_data:
            return JsonResponse({'status': 'error', 'message': 'Invalid authentication'}, status=401)

        # Proceed with user login
        tgID = user_data.get('id')
        username = user_data.get('username', f"tg_{tgID}")
        picture = user_data.get('photo_url', '')
        is_premium = user_data.get('is_premium', False)

        user, created = Myuser.objects.get_or_create(
            tgID=tgID,
            defaults={
                'username': username,
                'picture': picture,
                'is_premium': is_premium
                    }
        )
        
        login(request, user)
        return JsonResponse({'status': 'success', 'user': user.username})

    return render(request, 'home.html')