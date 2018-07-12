from django.db import models


# Create your models here.
class Personal(models.Model):
    personal_ID = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=20, blank=True)
    last_modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Personal"

class Header(models.Model):
    host_personal_ID = models.CharField(max_length=20, blank=True)
    guest_personal_ID = models.CharField(max_length=20, blank=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Header"

class Message(models.Model):
    header_id = models.IntegerField(blank=True)
    context = models.TextField(blank=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Message"


class Friendlist(models.Model):
    host_personal_ID = models.CharField(max_length=20, blank=True)
    hostfriendlist = models.TextField(blank=True)
    login_or_not = models.CharField(max_length=20, blank=True)
    friendrequest = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = "Friendlist"


