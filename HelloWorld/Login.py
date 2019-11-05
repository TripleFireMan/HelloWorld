#-*-coding:utf-8-*- 
#!/usr/bin/env python
# encoding: utf-8
'''
@author: 成焱
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: ab364743113@126.com
@file: Login.py
@time: 2019/11/5 4:48 PM
@desc:
'''
from django.http import HttpResponse
from TestModel.models import User
import json
def login(request):
    print(json.dumps(request.GET))
    return HttpResponse(['登录成功'])