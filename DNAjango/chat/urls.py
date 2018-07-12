#coding=utf-8
#  chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('<str:room_name>/', views.room, name='room'),
]

