#coding=utf-8


# 主要是在django admin的部分

from django import forms
from chat.models import Personal, Friendlist

class SignUpform(forms.ModelForm):
    username = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'id': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'email'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'id': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2'}))

    class Meta:
        model = Personal
        fields = ('username',)



# class AddFriendForm(forms.ModelForm):
#     friend_personalID =  forms.CharField(max_length=25,widget=forms.TextInput(attrs={'id':'fpid'}))
#     class Meta:
#         model = Friendlist
#         fields = ('requestnumbers',)
