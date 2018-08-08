from django.contrib.auth import models
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from django.http import HttpResponse
# 註冊用：
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# 導入表格，model的文檔:
from chat import forms
from chat.models import Personal
from chat.models import Check_Database_for_Send_friend_Request, Add_to_RequestCheck,\
    Parse_Request,Parse_Request_Accept_or_Reject,Check_Friendlist,From_username_to_Pid,\
    Check_Room_name_for_dialague,Check_Message_table,Get_room_name,Load_SenderLogs_From_Mysql,Load_ReceiverLogs_From_Mysql
#亂數密碼:
from uuid import uuid4
#csrf:
from django.views.decorators.csrf import csrf_exempt



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
        pu = pp.username

        #檢查好友清單：
        myfriend = Check_Friendlist(pid)

        if request.method == 'GET':
            # print('Get Get Get')
            if request.GET.get("logout"):
                logout(request)
                print('OUT GET')
                return redirect('/dna')

        if request.POST.get("logout"):
            logout(request)
            print('OUT POST')
            return redirect('/dna')


        # 交友需求：
        requestid = request.POST.get('idvalue')
        hostid = pid
        print('requestid:{}'.format(requestid))
        if requestid:
            requestid = requestid.strip()
            ans = Check_Database_for_Send_friend_Request(hostid, requestid)

            if ans!= None:
                if ans =='1':
                    ans543= "You Already Added !!"
                else:
                    ans543 = ans
            else:
                ans543 = "No User Exist"

            return HttpResponse(json.dumps({'ans543': ans543 }))

    return  render (request,'chat/main.html',locals())

@csrf_exempt
def main_for_ajax(request):
    ad = (request.POST.get('yes_to_add'))
    # ad_dic = {'yes_to_add': ad}
    if ad:
        requestid = request.POST.get('idvalue')
        requestid = requestid.strip()
        pp = Personal.objects.get(username = '{}'.format(str(request.user)))
        pid = (pp.personal_ID).strip()
        hostid = pid
        Add_to_RequestCheck(hostid,requestid)

    return JsonResponse({})





@csrf_exempt
def show_request(request):
    if request.user.is_authenticated:
        pp = Personal.objects.get(username = '{}'.format(str(request.user)))
        hostid = (pp.personal_ID)
        r= Parse_Request(hostid)
        h= [i for i in range(1,len(r)+1)]
        dic = dict(zip(h,r))
        print('交友需求字典:{}'.format(dic))
        return HttpResponse(json.dumps(dic))
    return -1


@csrf_exempt
def cry_or_smile(request):
    if request.user.is_authenticated:
    #  Get hostid:
        pp = Personal.objects.get(username = '{}'.format(str(request.user)))
        hostid = (pp.personal_ID)
    #  Get Rqquest id:
        what_you_click = request.POST.get('closeli')
        request_username = what_you_click.split('×O')[0]  # 會返回 XO字的按鈕 所以要把他split掉
        rid = Personal.objects.get(username = '{}'.format((request_username))) # 依樣用 .objects.get  去 MODEL資料庫找 personal id
        requestid = (rid.personal_ID)

        print(requestid)

        ad = (request.POST.get('cry_or_smile'))
        if ad == '0':
            print(ad)
            Parse_Request_Accept_or_Reject(0,hostid,requestid)
        elif ad == '1':
            print(ad)
            Parse_Request_Accept_or_Reject(1,hostid,requestid)
    return  JsonResponse({})




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
                if len(username)>=20:
                    messages.error(request,'username 長度請小於20')
                    return render(request, 'chat/signup.html', locals())
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




@csrf_exempt
def fire_in_the_hole_for_ajax(request):

    pp = Personal.objects.get(username = '{}'.format(str(request.user)))
    hostid = (pp.personal_ID)
    u_press = request.POST.get('fired_button')
    who_u_press = From_username_to_Pid(u_press)
    room_guys = Check_Room_name_for_dialague(hostid, who_u_press)
    print('who_u_press:{}'.format(who_u_press)) # freind_personal_id
    print('who_press:{}'.format(hostid))
    print('room_guys:{}'.format(room_guys))
    Check_Message_table(hostid, who_u_press)
    name = Get_room_name(hostid,who_u_press)
    name= name.split('-')
    table_name= ''
    for i in name :
        table_name=table_name+i
    ls= Load_SenderLogs_From_Mysql(table_name,hostid)
    print(ls)
    print('******************')
    ls.reverse()
    print(ls)

    print('')

    lr = Load_ReceiverLogs_From_Mysql(table_name, hostid)
    print(lr)
    print('%%%%%%%%%%%%%%%%%%')
    lr.reverse()
    print(lr)

    return JsonResponse({'room_guys':room_guys,
                         'lr':lr,
                         'ls':ls
                         })





def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


