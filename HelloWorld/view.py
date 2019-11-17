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
from TestModel.models import Book,BookCategory
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import pymysql
from django.forms.models import model_to_dict
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

def hello(request):
    context = {}
    context['hello'] = 'hello world'
    print(request)
    return render(request,'hello.html',context)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)


#获取书籍列表
@csrf_exempt
def bookList(request):

    # 获取请求页数
    page = request.GET.get('page',1)
    page = int(page)
    size = int(request.GET.get('size',10))
    category = request.GET.get('category','1')
    keywords = request.GET.get('keywords','')
    # 查询所有书籍列表
    booklist= Book.objects.all()
    booklist = Book.filterBooks(booklist,request)
    # 生成分页器
    paginate = Paginator(booklist,size)
    dict = {}
    dict['totalcount'] = paginate.count
    try:
        booklist = paginate.page(page)
    except EmptyPage:
        booklist = []
        print('empty page')
    except PageNotAnInteger:
        booklist = paginate.page(1)
        print('PageNotAnInteger')
    L = []
    for p in booklist:
        print(p,'++++=======')
        # p.downloadurl = 'http://ebooktest:8000/ebooks/%s/%s.txt' % p.name % p.name
        # print(p['downloadurl'],'----------------')
        b = model_to_dict(p)
        L.append(b)
    dict['code'] = '1'
    dict['message'] = '请求成功'
    dict['result'] = L
    return HttpResponse(json.dumps(dict,ensure_ascii=False,cls=DateEncoder))

@csrf_exempt
def category(request):
    categoryId = request.GET.get('category')
    categoryString = str(categoryId)
    bookCategory = BookCategory.objects.all()
    dic = {}
    List = []
    for c in bookCategory:
        d = model_to_dict(c)
        List.append(d)
    dic['code'] = '1'
    dic['message'] = '请求成功'
    dic['result'] = List
    print(dic)
    return HttpResponse(json.dumps(dic))

@csrf_exempt
def testwebhook(request):
    return HttpResponse('hehe')