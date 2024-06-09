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
from . import view,users
from django.contrib.staticfiles.views import serve
from django.urls import re_path,include
import DailyClock.views
from django.conf.urls.static import static
from HelloWorld import settings
from django.views.static import serve
from django.urls import path

from TYMetro.models import UserProfile
from DailyClock.models import DKJiTang
from rest_framework import routers, serializers, viewsets
# from django.conf import settings
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class JitangSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DKJiTang
        fields = '__all__'
class JitangViewSet(viewsets.ModelViewSet):
    queryset = DKJiTang.objects.all()
    serializer_class = JitangSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jitang',JitangViewSet)

def return_static(request, path, insecure=True, **kwargs):
    print(f'path==========={path}')
    
    return serve(request, path, insecure, **kwargs)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello',view.hello),
    url(r'^jianlong/codereview',view.jianlongCodeReview),
    # url(r'^users/userList',users.userList),
    url(r'^users/login', users.login),
    url(r'^users/register', users.register),
    url(r'^view/bookList',view.bookList),
    url(r'^view/category',view.category),
    url(r'^view/testwebhook', view.testwebhook),
    url(r'^view/sheetUpdate',view.sheetUpdate),
    url(r'^view/readBook',view.readBook),
    url(r'^view/chapters',view.chapters),
    url(r'^home',view.home),
    url(r'^lovehanjuTV',view.lovehanjuTV),
    url(r'^lovehanju',view.lovehanju),
    url(r'^duoduoplay',view.duoduoplay),
    url(r'^yangyang',view.yangyang),
    path('grappelli/',include('grappelli.urls')),
    # bugly统计
    url(r'^view/buglyReport', view.buglyReport),


    # 极简打卡APP使用接口
    url(r'^save_profile', DailyClock.views.save_profile, name='save_profile'),
    # 极简打卡url
    url(r'^dailyClock/',include('DailyClock.urls')),
    # 太原地铁项目url
    url(r'^ty_metro/',include('TYMetro.urls')),
    url(r'^ZhuaZhou/',include('ZhuaZhou.urls')),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),  # 添加这行
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^$', view.home),
    # url(r'^apple-app-site-association.json',TemplateView.as_view(template_name='apple-app-site-association.json')),
    url(r'^apple-app-site-association',view.apple_json),
    url(r'^files/', include('filer.urls')),
    path('api/', include(router.urls)),
    path('gitPull',view.gitPull),
    url(r'^api-auth/',include('rest_framework.urls')),
    # url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]

