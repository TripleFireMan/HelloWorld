#-*-coding:utf-8-*- 
#!/usr/bin/env python
# encoding: utf-8
'''
@author: 成焱
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: ab364743113@126.com
@file: users.py
@time: 2019/11/5 3:31 PM
@desc:
'''
from TestModel.models import Contact,User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


import json
@csrf_exempt
def userList(request):
    list = []
    result = Contact.objects.all()
    for user in result:
        dic = {'name':user.name,'age':user.age,'email':user.email}
        list.append(dic)
        print(user.name)
        print(user.age)
        print(user.email)
    jsonList = json.dumps(list)
    jsonString = str(jsonList)

    return HttpResponse([jsonString])
@csrf_exempt
def login(request):

    userName = request.POST.get('username')
    password = request.POST.get('password')

    try:
        obj = User.objects.get(username=userName)
        if obj.password == password:
            result = {'status': 'success', 'code': 0, 'data': {'uid': obj.id, 'username': userName, 'password': password}, 'message': '登录成功'}
            return HttpResponse([str(json.dumps(result))])
        else:
            result = {'status': 'success', 'code': -1,
                      'data': {},
                      'message': '登录失败,密码错误'}
            print(result)
            return HttpResponse([str(json.dumps(result))])
    except User.DoesNotExist:
        result = {'status': 'success', 'code': -1, 'data': {},
                  'message': '登录失败,用户不存在'}
        print(result)
        return HttpResponse([str(json.dumps(result))])


@csrf_exempt
def register(request):
    # jsonDumps = json.dumps(request.POST)
    print(request.POST)
    userName = request.POST.get('username')
    password = request.POST.get('password')


    print(userName,password)


    #数字字母,6-20正则表达式
    re_regist = r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$'

    try:
       obj = User.objects.get(username = userName)
       if obj != None:
           result = {'status': 'failed', 'code': -1, 'data': {}, 'message': '用户已存在'}
           return HttpResponse([str(json.dumps(result))])
       else:
            pass
    except User.DoesNotExist:
        user = User(username=userName, password=password)

        user.save()
        result = {'status': 'success', 'code': 0, 'data': {'uid':user.id, 'username': userName, 'password': password},
                  'message': '注册成功'}
        print(result)
        return HttpResponse([str(json.dumps(result))])





