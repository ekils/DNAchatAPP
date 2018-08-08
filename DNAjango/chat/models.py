from django.db import models, connection
from uuid import uuid4

# Create your models here.

# MYSQL :表格創建區

class Personal(models.Model):# 每個帳號的個人資訊
    personal_ID = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=20, blank=True)
    last_modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Personal"


# class Message(models.Model): # 聊天內容
#     header_id = models.IntegerField(blank=True)
#     context = models.TextField(blank=True)
#     last_modify_date = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = "Message"


class Friendlist(models.Model):# 好友單
    host_personal_ID = models.CharField(max_length=20, blank=True)
    hostfriendlist = models.CharField(max_length=20, blank=True)
    you_guys_chat_room_name= models.CharField(max_length=40, blank=True)

    class Meta:
        db_table = "Friendlist"


class RequestCheck(models.Model): # 好友確認
    host_personal_ID = models.CharField(max_length=20, blank=True)
    request_ID = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = "RequestCheck"
        unique_together =('host_personal_ID','request_ID')



# MYSQL :資料讀取區

def Check_Database_for_Send_friend_Request(hostid,requestid):
    with connection.cursor() as cursor:
        # 先確認有沒有該帳號：
        cursor.execute("select personal_ID from Personal")
        row = [(c) for c in cursor.fetchall() ]
        print('All user: {}'.format(row))

        get_one_or_nothing = None
        for ii in row:
            if requestid == ii[0]:

                # 先確認 好友名單有沒有此人： 有的話說已加過惹
                cursor.execute("select hostfriendlist from Friendlist where host_personal_ID= '{}'".format(hostid))
                cc = cursor.fetchall()
                listforcheck = [c[0] for c in cc]
                you_already_added = 0
                for i in listforcheck:
                    if requestid == i:
                        you_already_added = you_already_added + 1
                if you_already_added ==0:
                    # 把personal_ID 轉username 回傳 然後顯示在網頁上
                    cursor.execute("select username from Personal where personal_ID = '{}'".format(requestid))
                    get_one_or_nothing = cursor.fetchone()
                    print('Correct-Request:{}'.format(get_one_or_nothing[0]))
                    cursor.close()
                    return get_one_or_nothing
                else:
                    get_one_or_nothing = '1'
                    return get_one_or_nothing
            else:
                pass
        cursor.close()
        return get_one_or_nothing

def Add_to_RequestCheck(hostid,requestid):
    with connection.cursor() as cursor:

    # 把申請人的id 寫入到 RequestCheck ,對方確認後會update 相關資訊:
    # 這邊要注意， host:主人   request:申請者 所以如果是我申請，我會看到自己的id 顯示在 requestid 別搞混

        cursor.execute("insert into RequestCheck (host_personal_ID,request_ID) values ('{}','{}') on duplicate key update host_personal_ID ='{}', request_ID='{}' ".format(requestid,hostid,requestid,hostid))

    cursor.close()
    return

def Parse_Request(hostid):
    with connection.cursor() as cursor:
        cursor.execute("  select request_ID from  RequestCheck where host_personal_ID='{}'".format(hostid))
        temp_row = [c for c in cursor.fetchall()]
        row= []
        for ii in temp_row:
            row.append(ii[0])
        ruser=[]
        for i in row:
            cursor.execute("select username from Personal where personal_ID='{}'".format(i))
            temp_ruser = cursor.fetchone()
            ruser.append(temp_ruser[0])
    cursor.close()
    return ruser  # rows are string list

def Parse_Request_Accept_or_Reject(c_o_s,hostid,requestid):

    with connection.cursor() as cursor:
        if c_o_s ==1: # 接受交友
            print('Love')
            # 互為好友：
            # 增加彼此聊天室密碼：
            creat_room_name = str(uuid4())
            cursor.execute(" insert into Friendlist(host_personal_ID,hostfriendlist,you_guys_chat_room_name) values('{}','{}','{}')".format(hostid,requestid,creat_room_name))
            cursor.execute(" insert into Friendlist(host_personal_ID,hostfriendlist,you_guys_chat_room_name) values('{}','{}','{}')".format(requestid,hostid,creat_room_name))
            cursor.execute(" delete from RequestCheck where host_personal_ID = '{}'and request_ID ='{}'".format(hostid,requestid))

        elif c_o_s ==0: # 慘忍拒絕
            print('Damn')
            cursor.execute(" delete from RequestCheck where host_personal_ID = '{}'and request_ID ='{}'".format(hostid,requestid))
    cursor.close()
    return

def Check_Friendlist(hostid):
    with connection.cursor() as cursor:
        cursor.execute("select hostfriendlist from Friendlist where host_personal_ID= '{}' ".format(hostid))
        all_friends = cursor.fetchall()
        friendslist= [c[0] for c in all_friends]

        f_username_list= []
        for i in friendslist:
            cursor.execute("select username from Personal where  personal_ID= '{}' ".format(i))
            ff = cursor.fetchone()
            f_username = ff[0]
            f_username_list.append(f_username)
        print(f_username_list)
    cursor.close()
    return f_username_list


def From_username_to_Pid(username):
    with connection.cursor() as cursor:
        cursor.execute("select personal_ID from Personal where username = '{}' ".format(username))
        ff = cursor.fetchone()
        username_pid = ff[0]
    cursor.close()
    return username_pid


def Get_room_name(host_id,friend__personal_id): # 對話視窗編號
    with connection.cursor() as cursor:
        cursor.execute("select you_guys_chat_room_name from Friendlist where host_personal_ID ='{}' and hostfriendlist ='{}' ".format(host_id,friend__personal_id))
        get_name= cursor.fetchone()
        name = get_name[0]
    cursor.close()
    return name

def Check_Room_name_for_dialague(host_id,friend__personal_id): # 對話視窗所有人id

    name = Get_room_name(host_id,friend__personal_id)

    with connection.cursor() as cursor:
        cursor.execute("select host_personal_ID from Friendlist where you_guys_chat_room_name= '{}' ".format(name))
        all = cursor.fetchall()
        all_list= [c[0] for c in all]
    cursor.close()
    return all_list

def Check_Message_table(host_id, friend__personal_id):  # 創建對話紀錄表格
    name = Get_room_name(host_id, friend__personal_id)
    name= name.split('-')
    n= ''
    for i in name :
        n=n+i
    with connection.cursor() as cursor:
        cursor.execute("create table if not exists {}(id int NOT NULL AUTO_INCREMENT, Sender text NOT NULL,  Receiver text NOT NULL, Messages text  NOT NULL, Savetime Timestamp DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (id))".format(n))
    cursor.close()
    return


def Save_Messages(table_name,sender_id,receiver_id,content):
    with connection.cursor() as cursor:
        cursor.execute("alter table {} modify Messages MEDIUMTEXT character set utf8".format(table_name))  # 存入中文要先轉換utf8  MEDIUMTEXT:最多可以存到16mb長度
        cursor.execute("insert into {}(Sender,Receiver,Messages) values('{}','{}','{}')".format(table_name,sender_id,receiver_id,content))
    cursor.close()
    return


# def Load_MessageLogs_From_Mysql(table_name,sender_id,receiver_id):
#     with connection.cursor() as cursor:
#         cursor.execute("select Messages,Savetime from {} where Sender='{}' and Receiver='{}'".format(table_name,sender_id,receiver_id))
#         cc = [c for c in cursor.fetchall()] # 0:messages , 1: time
#         for i in cc:
#             print(i[0])
#         for i in cc:
#             print(i[1])
#
#     cursor.close()
#     return

def Load_SenderLogs_From_Mysql(table_name,sender_id):
    with connection.cursor() as cursor:
        cursor.execute("select Messages from {} where Sender='{}'".format(table_name,sender_id))
        cc = [c for c in cursor.fetchall()] # 0:messages , 1: time
        xx= []
        for ii in cc:
            xx.append(ii[0])
    cursor.close()
    return xx
def Load_ReceiverLogs_From_Mysql(table_name,receiver_id):
    with connection.cursor() as cursor:
        cursor.execute("select Messages from {} where Receiver='{}'".format(table_name,receiver_id))
        cc = [c for c in cursor.fetchall()]  # 0:messages , 1: time
        xx = []
        for ii in cc:
            xx.append(ii[0])
    cursor.close()
    return xx