#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:33 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.conf.urls import url,re_path
from SportRecord import views
from SportRecord.views import *
from django.urls import path
urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    # 运动配置接口
    path("config", ConfigView.as_view(), name="config"),
    path('jwt_test',TextView.as_view(), name='jwt_test'),
    path('login',LoginView.as_view(),name='login'),
    path("save", SaveView.as_view(), name="save"),#添加或者修改用户信息
    path("updatePwd", PwdView.as_view(), name="pwd"), # 修改密码
    path("uploadImage", AvatorView.as_view(), name="avator"),# 上传头像
    path("search", SearchView.as_view(), name="search"), # 获取用户列表
    path("resetPwd", ResetPwdView.as_view(), name="resetPwd"),#重置密码
    path("user", ActionView.as_view(), name="user"),# 操作用户信息
    path("checkUser", CheckView.as_view(), name="check"),# 检查用户名是否重复
    # 角色
    path("role", RoleView.as_view(), name="role"),#单个角色操作
    path("roleList", RoleListView.as_view(), name="RoleListView"),# 所有角色
    path("grantRole", GrantView.as_view(), name="GrantView"),# 授权
    path("roleSearch", RoleSearchView.as_view(), name="RoleSearchView"), #  角色查询
    # 菜单
    path("menuList", MenuListView.as_view(), name="MenuListView" ),
    path("grantMenu", GrantMenuView.as_view(), name="GrantMenuView"),
    path("menu/save", MenuView.as_view(), name="MenuView")
    
    
    # re_path(r'^templates/(?P<dynamic_part>[^/]+\.html)$', views.auto_template, name='auto_template'),
    # re_path(r'^users/<str:dynamic_part>',views.auto_template,name='auto_template')
]