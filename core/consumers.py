from channels.generic.websocket import WebsocketConsumer

class CampfireConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Broadcast the received message to all connected clients
        self.channel_layer.group_send(
            "campfire_group",
            {
                "type": "chat_message",
                "message": text_data,
            }
        )

    def chat_message(self, event):
        message = event["message"]
        # Send the message to WebSocket
        self.send(text_data=message)