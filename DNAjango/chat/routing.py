#coding=utf-8
from django.urls import path

from . import consumers,consumers2

websocket_urlpatterns = [
    path('fff/<str:room_name>/', consumers.ChatConsumer),
    path('fire_in_the_hole/<str:who_u_fire>/', consumers2.ChatConsumer), # main.html : new webcocket 後，會來這抓路徑 做handshaking
]