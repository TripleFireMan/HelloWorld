"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from django.conf.urls import url
# from . import view
#
# urlpatterns = [
#     url(r'^$', view.hello),
# ]

from django.conf.urls import url
from django.contrib import admin
from . import view,testdb,users
from django.contrib.staticfiles.views import serve
from django.urls import re_path
import DailyClock.views
from  HelloWorld import settings

def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello',view.hello),
    url(r'^justDoIt',view.testGouzi),
    url(r'^users/userList',users.userList),
    url(r'^users/login', users.login),
    url(r'^users/register', users.register),
    url(r'^view/bookList',view.bookList),
    url(r'^view/category',view.category),
    url(r'^view/testwebhook', view.testwebhook),
    url(r'^view/sheetUpdate',view.sheetUpdate),
    url(r'^view/readBook',view.readBook),
    url(r'^view/chapters',view.chapters),
    url(r'^home',view.home),

    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),  # 添加这行
    # 极简打卡APP使用接口
    # 问题反馈
    url(r'^dailyClock/feedBack',DailyClock.views.feedBack),
    # 版本历史记录
    url(r'^dailyClock/versionHistory',DailyClock.views.versionHistory),
    # 上传图片
    url(r'^dailyClock/index',DailyClock.views.index,name='index'),
    url(r'^save_profile',DailyClock.views.save_profile,name='save_profile'),
    # 隐私协议
    url(r'^dailyClock/private',DailyClock.views.private),
    # 用户协议
    url(r'^dailyClock/userProtocol', DailyClock.views.userProtocol),
    # 下载字体
    url(r'^dailyClock/fonts', DailyClock.views.fonts),
    # 今日卡片
    url(r'^dailyClock/todayCard',DailyClock.views.today_card),
    # bugly统计
    url(r'^view/buglyReport',view.buglyReport),
    url(r'^', view.home),
]