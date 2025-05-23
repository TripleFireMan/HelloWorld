# Generated by Django 3.2.25 on 2025-04-01 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ZhuaZhouModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('intrduce', models.CharField(max_length=255, verbose_name='介绍')),
                ('gender', models.CharField(blank=True, choices=[('男', '男'), ('女', '女')], max_length=20, verbose_name='性别')),
                ('img', filer.fields.image.FilerImageField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'verbose_name': '抓周数据',
                'verbose_name_plural': '抓周数据',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='标题')),
                ('img', filer.fields.image.FilerImageField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='carousel_image', to=settings.FILER_IMAGE_MODEL, verbose_name='抓周图片')),
            ],
            options={
                'verbose_name': '首页轮播图',
                'verbose_name_plural': '首页轮播图',
            },
        ),
    ]
