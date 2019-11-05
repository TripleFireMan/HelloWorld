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
from TestModel.models import Contact
from django.http import HttpResponse
import json

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

