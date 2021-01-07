#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:24 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos

from django.conf.urls import url
from TYMetro import views
from django.urls import path

urlpatterns = [
    url(r'^log110',views.log110),
    url(r'^getPhone',views.get_phone),
    url(r'^userLogin', views.user_login),
    path('bindUser',views.bindUser),
    url(r'^getInfo', views.get_info),
    path('modifireUserInfo',views.modifierUser),
]