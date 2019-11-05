#-*-coding:utf-8-*- 
#!/usr/bin/env python
# encoding: utf-8
'''
@author: 成焱
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: ab364743113@126.com
@file: testdb.py
@time: 2019/11/4 9:45 PM
@desc:
'''
from django.http import HttpResponse
from TestModel.models import Test
import json
def testdb(request):

    dic = {'name':'chengyan','age':22}
    jsondic = json.dumps(dic)
    jsonstr = str(jsondic)
    return HttpResponse([jsonstr])

    #新增数据
    # test1 = Test(name='chengyan')
    # test1.save()
    # return HttpResponse("<p>数据添加成功</p>")


    #查询数据
    # response = ''
    # response1 = ''
    # list = Test.objects.order_by("id").reverse()
    # response2 = Test.objects.get(id = 1)
    # response3 = Test.objects.filter(id = 1)
    # for var in list:
    #     response1 += var.name + ' '
    # response = response1
    # return HttpResponse("<p>"+response+"</p>")

    #修改数据
    # obj = Test.objects.get(id = 3)
    # obj.name = '成焱'
    # obj.save()
    # return HttpResponse("<p>"+obj.name+"</p>")

    #删除数据
    # obj = Test.objects.get(id = 3)
    # obj.delete()
    # return HttpResponse("<p>删除成功</p>")
