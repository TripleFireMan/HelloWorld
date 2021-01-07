from django.db import models

# Create your models here.
from django.db import models
from  django.utils import timezone
from  django.contrib.auth.models import AbstractUser
Gender_choice = (
    ('male','男'),
    ('female','女')
)

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称',default='')
    birthday = models.DateField(max_length=255,default=timezone.now)
    gender = models.CharField(max_length=6, verbose_name='性别', choices=Gender_choice)
    address = models.CharField(max_length=100,verbose_name='地址',default='')
    mobile = models.CharField(max_length=11,verbose_name='手机号',unique=True,default='')
    img = models.CharField(max_length=100,verbose_name='头像',default='')
    email = models.EmailField(max_length=200,verbose_name='邮箱',default='')
    username = models.CharField(max_length=50,verbose_name='用户名',default="",unique=True)
    password = models.CharField(max_length=50,verbose_name='密码',default='')
    third_source = models.CharField(max_length=50,verbose_name='来源',help_text='三方来源',default='')
    introduce = models.CharField(max_length=250,default='')
    apple_id = models.CharField(max_length=250,default='')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username