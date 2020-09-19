from django.db import models

# Create your models here.
from django.db import  models
from  django.utils import timezone

# 极简打卡App 问题反馈
class DKFeedBack(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=150)
    phoneNumber = models.CharField(max_length=20)
