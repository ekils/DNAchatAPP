#coding=utf-8
#  chat/urls.py
from django.urls import path
from . import views
from django.conf.urls import  url

urlpatterns = [
    # path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('main_for_ajax/',views.main_for_ajax,name= 'main_for_ajax'),
    path('show_request/',views.show_request,name= 'show_request'),
    path('cry_or_smile/',views.cry_or_smile,name= 'cry_or_smile'),
    path('chat_for_ajax/',views.chat_for_ajax,name= 'chat_for_ajax'),


    path('main/<str:room_name>/', views.room, name='room'),

]

