#coding=utf-8
import datetime
import pytz

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from chat.models import Get_room_name,From_username_to_Pid,Get_room_name,Save_Messages

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        igotu = (self.scope['url_route']['kwargs']['who_u_fire']).split('_')
        print('url_route:{}'.format(self.scope['url_route']))  # 去routing 的 websocket 抓route
        print(self.scope)
        # print('self.channel_name:{}'.format(self.channel_name))
        print('igotu:{}'.format(igotu))

        c= igotu[0]

        heyhey_pid = From_username_to_Pid(igotu[0])
        room_name= Get_room_name(igotu[1],heyhey_pid)
        self.room_group_name = room_name
    # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)    # channel＿name是隨機產生,不用管但一定要
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('歡慶88節')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

# 2. backend Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        messagex = text_data_json['messagex']
        user = str(self.scope['user'])
        timezone = pytz.timezone('Asia/Taipei')
        now_time = datetime.datetime.now(timezone).strftime('%H:%M')
        print('text_data_json :{}'.format(text_data_json))
        print('user:{}'.format(user))
        print('now_time:{}'.format(now_time))

    # 3. Then Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messagex': messagex,
                'user': user,
                'now_time': now_time
            }
        )

# 4. Receive message from room group
    def chat_message(self, event):
        messagex = event['messagex']
        now_time = event['now_time']
        user = event['user']
        print('messagex :{}'.format( messagex))


        igotu = (self.scope['url_route']['kwargs']['who_u_fire']).split('_')
        heyhey_pid = From_username_to_Pid(igotu[0])
        name = Get_room_name(igotu[1], heyhey_pid)
        name= name.split('-')
        room_name= ''
        for i in name:
            room_name = room_name+i

        Save_Messages(room_name, igotu[1], heyhey_pid, messagex)

    # 5. Send message to WebSocket (frontend)
        self.send(text_data=json.dumps({
            'messagex': messagex,
            'user': user,
            'now_time': now_time,
        }))

