from channels.generic.websocket import WebsocketConsumer
import secrets
import string
from core.models import Myuser
from asgiref.sync import async_to_sync

from myspace import settings

def generate_random_code():
    # This generates a string of 6 random digits (0-9)
    return ''.join(secrets.choice(string.digits) for _ in range(6))
import urllib.parse
import hmac
import hashlib
import json

import urllib.parse
import hmac
import hashlib
import json

import urllib.parse
import hmac
import hashlib
import json

def verify_telegram_web_app(raw_init_data, bot_token):
    # 1. Parse the query string properly. 
    # Do NOT include the 'initData=' prefix if your variable already contains the full string.
    # If the input still has 'initData=', strip it first:
    if raw_init_data.startswith("initData="):
        raw_init_data = raw_init_data.split("initData=", 1)[1]
    
    # 2. Decode the URL-encoded string once
    decoded_string = urllib.parse.unquote(raw_init_data)
    
    # 3. Parse into a dictionary
    parsed_data = urllib.parse.parse_qs(decoded_string)
    
    if 'hash' not in parsed_data:
        return None
    
    # 4. Extract hash and sort keys alphabetically
    received_hash = parsed_data.pop('hash')[0]
    sorted_keys = sorted(parsed_data.keys())
    
    # 5. Build the data_check_string exactly as Telegram requires:
    # key1=value1\nkey2=value2...
    data_check_list = []
    for key in sorted_keys:
        data_check_list.append(f"{key}={parsed_data[key][0]}")
    data_check_string = "\n".join(data_check_list)
    
    # 6. Generate the secret key (HMAC-SHA256 of "WebAppData" with your bot token)
    secret_key = hmac.new(
        "WebAppData".encode(), 
        bot_token.encode(), 
        hashlib.sha256
    ).digest()
    
    # 7. Generate the hash to compare
    calculated_hash = hmac.new(
        secret_key, 
        data_check_string.encode(), 
        hashlib.sha256
    ).hexdigest()
    
    # Compare
    if hmac.compare_digest(calculated_hash, received_hash):
        return json.loads(parsed_data['user'][0])
    
    return None
# Example usage:
code = generate_random_code()
campid=[]
campstat={}
print(f"Your 6-digit code is: {code}")
class CampfireConsumer(WebsocketConsumer):
    def connect(self):
        # 1. Get query string
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_data = urllib.parse.parse_qs(query_string)
        
        # 2. Extract initData
        init_data = query_data.get('initData', [None])[0]
        
        if init_data:
            print(settings.BOT_APIKEY)
            # VALIDATION: Use your function
            user_data = verify_telegram_web_app(init_data, settings.BOT_APIKEY)
            
            # CRITICAL: Check if user_data is actually a dictionary
            if user_data and isinstance(user_data, dict):
                self.tgID = user_data.get('id')
                if user_data.get('username') is None or user_data.get('username') == "":
                    self.username = f"User{self.tgID}"
                self.username = user_data.get('username')
                self.first_name = user_data.get('first_name')
                if len(campid)==0:
                    print("DEBUG: No existing camp, creating new one.")
                    self.camp_id = generate_random_code()
                    campid.append(self.camp_id)
                    campstat[self.camp_id]={"users":1, "usernames":[self.username]}
                
                # Join the group
                    async_to_sync(self.channel_layer.group_add)(self.camp_id,
                                                             self.channel_name)
                
                    self.accept()
                    print(f"DEBUG: User {self.username} connected to camp {self.camp_id} usernames in camp: {campstat[self.camp_id]['usernames']}")
                    return async_to_sync(self.channel_layer.group_send)(
                        self.camp_id,
                        {
                            "type": "user_joined",
                            "message": f"{self.username} has joined the campfire!",
                            'user': self.username,
                            'camp_id': self.camp_id,
                            'users_in_camp': campstat[self.camp_id]["users"],
                            'usernames_in_camp': campstat[self.camp_id]["usernames"],
                        }
                    )
                else:
                    self.camp_id=campid[0]
                    if campstat[self.camp_id]["users"]<5:
                        campstat[self.camp_id]["users"]+=1
                        campstat[self.camp_id]["usernames"].append(self.username)
                        async_to_sync(self.channel_layer.group_add)(self.camp_id,
                                                                self.channel_name)
                
                        self.accept()
                        print(f"DEBUG: User {self.username} joined existing camp {self.camp_id}. Total users now: {campstat[self.camp_id]['users']} Usernames: {campstat[self.camp_id]['usernames']}")
                        return async_to_sync(self.channel_layer.group_send)(
                        self.camp_id,
                        {
                            "type": "user_joined",
                            "message": f"{self.username} has joined the campfire!",
                            'user': self.username,
                            'camp_id': self.camp_id,
                            'users_in_camp': campstat[self.camp_id]["users"],
                            'usernames_in_camp': campstat[self.camp_id]["usernames"],
                        }
                    )
                    else:
                        self.camp_id=generate_random_code()
                        campid[0]=self.camp_id
                        campstat[self.camp_id]={"users":1, "usernames":[self.username]}
                        async_to_sync(self.channel_layer.group_add)(self.camp_id,
                                                                self.channel_name)
                        self.accept()
                        return async_to_sync(self.channel_layer.group_send)(
                        self.camp_id,
                        {
                            "type": "user_joined",
                            "message": f"{self.username} has joined the campfire!",
                            'user': self.username,
                            'camp_id': self.camp_id,
                            'users_in_camp': campstat[self.camp_id]["users"],
                            'usernames_in_camp': campstat[self.camp_id]["usernames"],
                        }
                    )
            else:
                print("DEBUG: Validation returned None or invalid data")

        # Reject if anything went wrong
        self.close()
   
    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            async_to_sync(self.channel_layer.group_send)(
                self.camp_id,
                {
                    "type": "voice_stream",
                    "bytes": bytes_data,
                    "sender_channel": self.channel_name,
                    'user': self.username
                }
            )
            return

        data_type=json.loads(text_data).get('type')
        if data_type=="chat":
            data = json.loads(text_data)
            message=data.get('message')
            print(f"DEBUG: Received chat message: {message} from user: {self.username} in camp {self.camp_id}")
            async_to_sync(self.channel_layer.group_send)(
                self.camp_id,
                {
                    "type": "chat",
                    "message": message,
                    'user': data.get('user'),
                }
            )
        elif data_type=="mic_status":
            data = json.loads(text_data)
            mic_status=data.get('status')
            print(f"DEBUG: Received mic status: {mic_status} from user: {self.username} in camp {self.camp_id}")
            async_to_sync(self.channel_layer.group_send)(
                self.camp_id,
                {
                    "type": "mic_status",
                    "mic_status": mic_status,
                    'user': data.get('user'),
                }
            )
    def disconnect(self, close_code):
        campstat[self.camp_id]["users"]-=1
        campstat[self.camp_id]["usernames"].remove(self.username)
        async_to_sync(self.channel_layer.group_send)(self.camp_id,
                                                 {  
                                                     "type": "user_left",
                                                     "message": f"{self.username} has left the campfire.",
                                                     'user': self.username,
                                                     'camp_id': self.camp_id,
                                                 })
        pass

    def chat(self, event):
        message = event["message"]
        user = event["user"]
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'user': user
        }))
    def voice_stream(self, event):
        if self.channel_name != event["sender_channel"]:
            
            username = event["user"]                       # the speaker's username
            name_bytes = username.encode("utf-8")
            header = bytes([len(name_bytes)]) + name_bytes  # 1 byte length + UTF-8 name
            self.send(bytes_data=header + event["bytes"])
    def mic_status(self, event):
        mic_status = event["mic_status"]
        print(f"DEBUG: Broadcasting mic status: {mic_status} to camp {self.camp_id}")
        user = event["user"]
        # Send the mic status to WebSocket
        self.send(text_data=json.dumps({
            'type': 'mic_status',
            'mic_status': mic_status,
            'user': user
        }))
    def user_left(self, event):
        message = event["message"]
        print(f"DEBUG: Broadcasting message: {message} to camp {self.camp_id}")
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'user_left',
            'message': message,
            'user': event['user'],
            'camp_id': event['camp_id'],
        }))
    def user_joined(self, event):
        message = event["message"]
        print(f"DEBUG: Broadcasting message: {message} to camp {self.camp_id} with users: {event['usernames_in_camp']}")
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'user_joined',
            'message': message,
            'user': event['user'],
            'camp_id': event['camp_id'],
            'users_in_camp': event['users_in_camp'],
            'usernames_in_camp': event['usernames_in_camp'],
        }))