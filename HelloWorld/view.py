#-*-coding:utf-8-*- 
#!/usr/bin/env python
# encoding: utf-8
'''
@author: 成焱
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: ab364743113@126.com
@file: view.py
@time: 2019/11/4 12:53 PM
@desc:
'''

from django.http import HttpResponse
from django.shortcuts import render
def hello(request):
    context = {}
    context['hello'] = 'hello world'
    return render(request,'hello.html',context)