from django.db import models

# Create your models here.
from  django.db import models
from  django.utils import timezone
import os

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
    read_url = models.CharField(max_length=255, default='')
    des = models.CharField(max_length=1000, default='')
    image = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='')
    author = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=255, default='')
    update_time = models.DateField(max_length=255, default=timezone.now())
    latest_chapter_name = models.CharField(max_length=255, default='')
    latest_chapter_url = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=1000, default='')
    download_url = models.CharField(max_length=255, default='')
    isUpload = models.BooleanField(default=False)
    bookCategory = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name

    def filterBooks(objects,request):
        category = request.GET.get('category')
        keywords = request.GET.get('keywords')
        print(category)
        if category:
            if str(category) == '7':
                print(category)
                objects = objects.filter(status__icontains='完本')
            else:
                objects = objects.filter(bookCategory_id=category)
        if keywords:
            title_objects = objects.filter(name__icontains=keywords)
            author_objects = objects.filter(author__icontains=keywords)
            descrotion_objects = objects.filter(des__icontains=keywords)
            objects = author_objects | title_objects | descrotion_objects
        objects = objects.order_by('-update_time')
        return objects

class Chapter(models.Model):
    name = models.CharField(max_length=255,default='')
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    path = models.CharField(max_length=255,default='')
    chaperIdx =models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

    def filterChapters(objects,request):
        bookid = request.GET.get('bookId',3978)
        print(bookid)
        chaptid = request.GET.get('chapterId',0)
        chaptid = int(chaptid)
        if bookid:
            objects = objects.filter(book_id=bookid)

        if chaptid == 0:
                objects = objects.filter(chaperIdx=chaptid) | objects.filter(chaperIdx=chaptid + 1)
        else:
            objects = objects.filter(chaperIdx=chaptid) | objects.filter(chaperIdx=chaptid - 1) | objects.filter(
                chaperIdx=chaptid + 1)
        return objects

    def filterAllChapters(objects,request):
        bookid = request.GET.get('bookId', 3978)
        if bookid:
            objects = objects.filter(book_id=bookid)
        return objects
class SearchHistory(models.Model):
    keyword = models.CharField(max_length=255,default='')
    count= models.IntegerField(default=1)
    def __unicode__(self):
        return self.keyword

class BookSheet(models.Model):
    bookids = models.CharField(max_length=255, default='')
    bookNames = models.CharField(max_length=255,default='')
    userid = models.CharField(max_length=255,default='')
    def __unicode__(self):
        return self.bookids





