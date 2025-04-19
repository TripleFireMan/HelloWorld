#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:33 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.conf.urls import url,re_path,include
from SportRecord import views
from SportRecord.views import *
from django.urls import path
from rest_framework import viewsets,serializers,routers

router = routers.DefaultRouter()
router.register(r'users',SRUserViewSet)
router.register(r'record',SportRecordViewSet)
router.register(r'partner',PartnerViewSet)
router.register(r'place',PlaceViewSet)
router.register(r'role',RoleViewSet)# 角色
router.register(r'property',PropertyViewSet)# 道具
router.register(r'clothing',ClothingViewSet) #  服装
router.register(r'photo',PhotoViewSet) #图片
router.register(r'mood',MoodViewSet) #心情
router.register(r'users/(?P<uid>\d+)/places', UserPlaceViewSet, basename='user-places') # 给用户添加地点
router.register(r'users/(?P<uid>\d+)/partners', UserPartnerViewSet, basename='user-partners') # 给用户添加伴侣
urlpatterns = [
    path("api/", include(router.urls)),
    path("home", HomeView.as_view(), name="home"),
    # 运动配置接口
    path("config", ConfigView.as_view(), name="config"),
    path('jwt_test',TextView.as_view(), name='jwt_test'),
    path('login',LoginView.as_view(),name='login'),
    # 菜单
    path("menuList", MenuListView.as_view(), name="MenuListView" ),
    path("grantMenu", GrantMenuView.as_view(), name="GrantMenuView"),
    path("menu/save", MenuView.as_view(), name="MenuView"),
    # re_path(r'^templates/(?P<dynamic_part>[^/]+\.html)$', views.auto_template, name='auto_template'),
    # re_path(r'^users/<str:dynamic_part>',views.auto_template,name='auto_template')
]