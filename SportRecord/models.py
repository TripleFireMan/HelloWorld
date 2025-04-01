from django.db import models
from django.utils.translation import gettext_lazy as _
from system.storage import ImageStorage
from datetime import datetime

ChooseType = (
    ('za','za'),
    ('zw','zw'),
    ('my','my')
)

GenderType = (
    ('男','男'),
    ('女','女')
)

class SRUserProfile(models.Model):
    name = models.CharField(default='', max_length=50,blank=True, null=True, verbose_name='姓名')
    avator = models.ImageField(default='',upload_to='sportRecord/%Y/%m/%d',storage=ImageStorage, blank=True, null=True,verbose_name='头像')
    address = models.CharField(_("地址"), max_length=50,default='')
    birthday = models.DateField(_("出生日期"),editable=True,default=datetime.now)
    created = models.DateTimeField(_("创建日期"), auto_now_add=True)
    updated = models.DateTimeField(_("更新时间"), auto_now=True)
    partner = models.ForeignKey("SRPartner", verbose_name=_("伴侣"), on_delete=models.CASCADE,default=None)
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    
class SRSportCategory(models.Model):
    name = models.CharField(_("名称"), max_length=50,blank=True, null=True)
    icon = models.FileField(_("图标"), upload_to='sportRecord/category', max_length=100,blank=True, null=True)
    class Meta:
        verbose_name = '运动类型'
        verbose_name_plural = '运动类型'
    def __str__(self):
        return self.name

class SRUserSportRecord(models.Model):
    name = models.CharField(_("行为名称"), max_length=50, blank=True, null=True)
    address = models.CharField(_("行为地点"), max_length=50, blank=True, null=True)
    duration = models.IntegerField(_("持续时间"), blank=True, null=True)
    type = models.CharField(_("类型"), max_length=50, choices=ChooseType,default='',blank=True, null=True)
    category = models.ForeignKey(SRSportCategory, verbose_name=_("分类"), on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    
class SRPartner(models.Model):
    name = models.CharField(_("昵称"), max_length=50,default='')
    birthday = models.DateField(_("生日"),default=datetime.now)
    gender = models.CharField(_("性别"), max_length=50,choices=GenderType,default='')
    mobile = models.CharField(_("手机号"), max_length=50,default='')
    avator = models.ImageField(_("头像"), upload_to='sportRecord/%Y/%m/%d', height_field=None, width_field=None, max_length=None,default=None)
    remark = models.CharField(_("备注"), max_length=50,default='')
    class Meta:
        verbose_name = '伴侣'
        verbose_name_plural = '伴侣'
    def __str__(self):
        return self.name
    
class SRProperty(models.Model):
    name = models.CharField(_("名称"), max_length=50)
    icon = models.ImageField(_("图标"), upload_to="sportRecod/%Y%m%d", height_field=None, width_field=None, max_length=None, default=None)
    bgColor = models.CharField(_("背景色"), max_length=50)
    class Meta:
        verbose_name = '道具'
        verbose_name_plural = '道具'
    def __str__(self):
        return self.name

class SRSystemConfig(models.Model):
    name = models.CharField(_("应用名称"), max_length=50)
    isInAppStoreView = models.BooleanField(_("是否在审核"))
    class Meta:
        verbose_name = '系统配置接口'
        verbose_name_plural = '系统配置接口'
    def __str__(self):
        return self.name
    