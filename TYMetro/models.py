from django.db import models

# Create your models here.
from django.db import models
from  django.utils import timezone
from  django.contrib.auth.models import AbstractUser

import datetime
Gender_choice = (
    ('男','男'),
    ('女','女')
)


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称',default='',blank=True)
    birthday = models.DateField(max_length=255,default=timezone.now,blank=True)
    gender = models.CharField(max_length=6, verbose_name='性别', choices=Gender_choice,blank=True)
    address = models.CharField(max_length=100,verbose_name='地址',default='',blank=True)
    mobile = models.CharField(max_length=11,verbose_name='手机号',unique=True,default='')
    img = models.CharField(max_length=100,verbose_name='头像',default='',blank=True)
    email = models.EmailField(max_length=200,verbose_name='邮箱',default='',blank=True)
    username = models.CharField(max_length=50,verbose_name='用户名',default="",unique=True)
    password = models.CharField(max_length=200,verbose_name='密码',default='')
    third_source = models.CharField(max_length=50,verbose_name='来源',help_text='三方来源',default='',blank=True)
    introduce = models.CharField(max_length=250,default='',blank=True)
    apple_id = models.CharField(max_length=250,default='',blank=True)

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        if self.nick_name:
            return self.nick_name
        elif self.mobile:
            return self.mobile
        else:
            return self.username


class FeedBack(models.Model):
    feed_text = models.CharField(max_length=1000, verbose_name='反馈', blank=True)
    feed_imgs = models.CharField(max_length=1000, verbose_name='图片', blank=True)
    create_at = models.DateField(max_length=255, default=timezone.now, blank=True)
    update_at = models.DateField(max_length=255, default=timezone.now, blank=True)

    class Meta:
        verbose_name='问题反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.feed_text