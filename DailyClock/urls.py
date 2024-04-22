#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:33 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.conf.urls import url,re_path
from DailyClock import views
from django.urls import path
urlpatterns = [
    # 问题反馈
    url(r'^feedBack', views.feedBack),
    # 版本历史记录
    url(r'^versionHistory', views.versionHistory),
    path('userProfile.html',views.indexClock),
    # 上传图片
    url(r'^index', views.index, name='index'),
    # 隐私协议
    url(r'^private', views.private),
    # 用户协议
    url(r'^userProtocol', views.userProtocol),
    # 下载字体
    url(r'^fonts', views.fonts),
    # 今日卡片
    url(r'^todayCard', views.today_card),
    url('test.html',views.test),
    url(r'^userLogin', views.user_login),
    re_path(r'^templates/(?P<dynamic_part>[^/]+\.html)$', views.auto_template, name='auto_template'),
    
    # re_path(r'^users/<str:dynamic_part>',views.auto_template,name='auto_template')
]