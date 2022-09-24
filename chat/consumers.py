import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from core.models import ChatMessage
from django.contrib.auth.models import User

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name,
#         )
#         self.accept()
        
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
        
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
    
#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps({
#             'type': 'chat',
#             'message': message
#         }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.userId = 'roomId' + self.scope['url_route']['kwargs']['userId']
        self.userId_group_name = 'chat_%s' % self.userId
        await self.channel_layer.group_add(
            self.userId_group_name,
            self.channel_name,
        )
        await self.accept()
        
    # async def disconnect(self):
    #     await self.channel_layer.group_discard(
    #         self.userId_group_name,
    #         self.channel_name,
    #     )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        userId = data['userId']
        requestUser = data['requestUser']
        
        await self.save_message(requestUser, userId, message)
        
        await self.channel_layer.group_send(
            self.userId_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'requestUser': requestUser,
                'userId': userId,
            }
        )
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        requestUser = event['requestUser']
        userId = event['userId']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'requestUser': requestUser,
            'userId': userId,
        }))
        
    @sync_to_async
    def save_message(self,requestUser, userId, message):
        to_user = User.objects.get(id=userId)
        requestUser = User.objects.get(id=requestUser)
        message = ChatMessage.objects.create(from_user=requestUser, to_user=to_user, message=message)
        message.save()
        