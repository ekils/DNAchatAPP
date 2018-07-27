#coding=utf-8

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from chat.models import Get_room_name

class ChatConsumer(WebsocketConsumer):


    def connect(self):
        igotu = (self.scope['url_route']['kwargs']['who_u_fire']).split('_')
        print('url_route:{}'.format(self.scope['url_route']))  # 去routing 的 websocket 抓route
        # print('self.channel_name:{}'.format(self.channel_name))
        # print('igotu:{}'.format(igotu))
        room_name= Get_room_name(igotu[1],igotu[0])
        self.room_group_name = room_name
    # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)    # channel＿name是隨機產生,不用管但一定要
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

# 2. backend Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        messagex = text_data_json['messagex']
        print('text_data_json :{}'.format(text_data_json))

    # 3. Then Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messagex': messagex
            }
        )

# 4. Receive message from room group
    def chat_message(self, event):
        messagex = event['messagex']

    # 5. Send message to WebSocket (frontend)
        self.send(text_data=json.dumps({
            'messagex': messagex
        }))

