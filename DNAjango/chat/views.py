from django.contrib.auth import models
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from chat import forms
from chat.models import Personal
from django.contrib.auth.hashers import make_password
from uuid import uuid4

from django.views.decorators.csrf import csrf_exempt

from django.db import connection, transaction

def login(request):
    template = 'chat/login.html'
    if request.method == 'GET':
        return render(request, template)

    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        print( '請填資料')
        return render(request, template)

    user = authenticate(username=username, password=password)

    if not user:  # authentication fails
        messages.error(request, '登入失敗 確認帳號密碼是否輸入正確')
        return render(request, template, {})


    # login success
    auth_login(request, user)
    print( '登入成功')
    if request.user.is_authenticated:
        print("{} is Logged in".format(username))
    else:
        print("Not logged in")
    return redirect('/dna/main')

@csrf_exempt
def main(request):
    if request.user.is_authenticated:
        print('User "{}" is in the main page.'.format(str(request.user)))
        pp = Personal.objects.get(username = '{}'.format(str(request.user)))
        pid = (pp.personal_ID)



    if request.method == 'GET':
        print('Get Get Get')
        if request.GET.get("logout"):
            logout(request)
            print('OUT GET')
            return redirect('/dna')
    else:
        print('Post Post Post')

       # 交友需求：
        if request.is_ajax():

            print(request.POST.get('idvalue'))


        if request.POST.get("logout"):
            logout(request)
            print('OUT POST')
            return redirect('/dna')
    return  render (request,'chat/main.html',locals())


def signup(request):
    if request.method == "POST":
        register_form = forms.SignUpform(request.POST)
        if register_form.is_valid(): # 表格要全寫才叫vaild
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password2']

            if password != password2:
                messages.error(request,'請檢查密碼是否輸入正確')
                return render(request, 'chat/signup.html', locals())
            if len(password)< 8 :
                messages.error(request,'密碼長度需至少8個字元')
                return render(request, 'chat/signup.html', locals())

            else:
                same_name_user = models.User.objects.filter(username = username)
                if same_name_user:
                    messages.error(request,'用戶已經存在，請更換')
                    return render(request, 'chat/signup.html', locals())
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    messages.error(request,'該信箱已經註冊過，請更換')
                    return render(request, 'chat/signup.html', locals())

                new_user = models.User()
                new_user.username = username
                # new_user.password = password
                new_user.password = make_password(password)
                new_user.email = email
                new_user.save()
                print('Sign up Done')

                if request.POST.get('username'):
                    un = Personal()
                    un.username = request.POST.get('username')

                    pid = str(uuid4())
                    personal_id = pid.split('-')[4]
                    un.personal_ID = personal_id
                    un.save()
                return redirect('/dna')

    register_form = forms.SignUpform()
    return render(request, 'chat/signup.html',{})



def logout(request):
    print('{} is log out'.format(request.user))
    auth_logout(request)


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


