#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:24 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache
from django.forms.models import model_to_dict
import json
from SportRecord.models import *

# Create your views here.

def getUsers(request):
        return HttpResponse('123')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # uid = request.GET.get('uid')
        result = {}
        result['code'] = 200
        result['message'] = '请求成功'
        # result['uid'] = uid
        # result['args'] = args
        # result['kwargs'] = request.GET
        data = {}
        # 查询道具信息
        propertys = SRProperty.objects.values('name','icon','bgColor')
        data['propertys'] = list(propertys)
        # 查询分类信息
        categorys = SRSportCategory.objects.values('name','icon')
        data['categorys'] = list(categorys)
        result['data'] = data
        
        return HttpResponse(json.dumps(result))

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')


class ConfigView(View):
    def get(self, request, *args, **kwargs):
        
        result = {}
        result['code'] = 200
        result['message'] = '请求成功'

        data = {}
        # 查询道具信息
        propertys = SRProperty.objects.values('name','icon','bgColor')
        data['propertys'] = list(propertys)
        # 查询分类信息
        categorys = SRSportCategory.objects.values('name','icon')
        data['categorys'] = list(categorys)
        # 查询系统配置
        config = SRSystemConfig.objects.get(name='运动记录')
        config_dic = model_to_dict(config)
        del config_dic['id']
        data['config'] = config_dic
        result['data'] = data
        
        return HttpResponse(json.dumps(result))

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')