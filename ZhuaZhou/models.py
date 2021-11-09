from django.db import models
from filer.fields.image import FilerImageField
# Create your models here.
Gender_choice = (
    ('男','男'),
    ('女','女')
)
class ZhuaZhouModel(models.Model):
    name = models.CharField(max_length=255,verbose_name='名称')
    intrduce = models.CharField(max_length=255,verbose_name='介绍')
    gender = models.CharField(max_length=20,choices=Gender_choice,blank=True,verbose_name='性别')
    img =  FilerImageField(related_name='product_image',on_delete=models.CASCADE,blank=True)
    class Meta:
        verbose_name='抓周数据'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 轮播图
class Carousel(models.Model):
     title = models.CharField(max_length=255,blank=True,verbose_name='标题')
     img = FilerImageField(related_name='carousel_image',on_delete=models.CASCADE,blank=True,verbose_name='抓周图片')
     class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name
     def __str__(self):
         return self.title
