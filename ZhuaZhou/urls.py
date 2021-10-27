#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 4:40 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.conf.urls import url
from ZhuaZhou import views
from django.urls import path
urlpatterns = [
    url(r'^Tools',views.tools)
]