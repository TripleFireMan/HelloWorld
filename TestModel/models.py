from django.db import models

# Create your models here.
from  django.db import models
from  django.utils import timezone

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

class BookCategory(models.Model):
    name = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.name

class Book(models.Model):
    link = models.CharField(max_length=255,default='')
    image = models.CharField(max_length=255, default='')
    pic = models.CharField(max_length=255,default='')
    title = models.CharField(max_length=255, default='')
    desciption = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    author = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    status = models.BooleanField(default=False)
    author_link = models.CharField(max_length=255, default='')
    update_time = models.DateField(max_length=255, default=timezone.now())
    downloadurl = models.CharField(max_length=255, default='')
    file_url    = models.CharField(max_length=255, default='')
    bookCategory = models.ForeignKey(BookCategory,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name

    def filterBooks(objects,request):
        category = request.GET.get('category')
        keywords = request.GET.get('keywords')
        print(category)
        if category:
            objects = objects.filter(bookCategory_id=category)
        if keywords:
            title_objects = objects.filter(title__icontains=keywords)
            author_objects = objects.filter(author__icontains=keywords)
            descrotion_objects = objects.filter(desciption__icontains=keywords)
            objects = author_objects | title_objects | descrotion_objects
        return objects

class Chapter(models.Model):
    name = models.CharField(max_length=255,default='')
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    path = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.name





