from django.db import models

# Create your models here.
from  django.db import models
import datetime
class Test(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=200,default="",editable=False)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=20)
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE,)
    def __unicode__(self):
        return self.name

class User(models.Model):
    #用户名
    username = models.CharField(max_length=50, default='')
    #密码
    password = models.CharField(max_length=10,default='')
    #昵称
    nickname = models.CharField(max_length=50,default='')
    #头像
    avtor = models.URLField()
    #三方登录微信
    wx_openid = models.CharField(max_length=100,default='')
    wx_avtor = models.CharField(max_length=100,default='')
    wx_access_token = models.CharField(max_length=100,default='')
    wx_unionid = models.CharField(max_length=100,default='')
    wx_refresh_token = models.CharField(max_length=100, default='')
    wx_city = models.CharField(max_length=100, default='')
    wx_headimgurl = models.CharField(max_length=100, default='')
    wx_language = models.CharField(max_length=100, default='')
    wx_province = models.CharField(max_length=100, default='')
    wx_nickname = models.CharField(max_length=100, default='')
    wx_sex = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nickname

class Book(models.Model):
    link = models.CharField(max_length=255,default='')
    image = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    desciption = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    author = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    status = models.BooleanField(default=False)
    author_link = models.CharField(max_length=255, default='')
    update_time = models.DateField(max_length=255, default=datetime.datetime.now())
    downloadurl = models.CharField(max_length=255, default='')
    def __unicode__(self):
        return self.name

