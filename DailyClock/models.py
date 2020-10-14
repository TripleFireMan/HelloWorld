from django.db import models

# Create your models here.
from django.db import  models
from  django.utils import timezone
from django import forms
from system.storage import ImageStorage


# 极简打卡App 问题反馈
class DKFeedBack(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    date = models.DateField(max_length=255,default=timezone.now)

class DKVersionHistory(models.Model):
    version = models.CharField(max_length=10)
    des = models.CharField(max_length=150)
    date = models.DateField(max_length=10,default=timezone.now)

class DKFonts(models.Model):
    name = models.CharField(max_length=50, default='')
    font_name = models.CharField(max_length=30, default='')
    font_bold_name = models.CharField(max_length=20, default='')
    url = models.CharField(max_length=100, default='')

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100,label='名字:',required=False)
    picture = forms.ImageField(label='图片:')

class Profile(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100,default="")
    picture = models.ImageField(upload_to='img/%Y/%m/%d',storage= ImageStorage())
    feedBackInfo = models.ForeignKey(DKFeedBack,on_delete= models.CASCADE,default=1)
    class Meta:
        db_table = 'profile'
    def __str__(self):
        return self.name

class Result(models.Model):
    status = models.CharField(max_length=10,default=0)
    message = models.CharField(max_length=20,default='success')


