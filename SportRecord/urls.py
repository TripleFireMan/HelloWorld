#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:33 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.conf.urls import url,re_path
from SportRecord import views

from django.urls import path
urlpatterns = [
    url(r"^Users", views.getUsers),
    # re_path(r'^templates/(?P<dynamic_part>[^/]+\.html)$', views.auto_template, name='auto_template'),
    # re_path(r'^users/<str:dynamic_part>',views.auto_template,name='auto_template')
]