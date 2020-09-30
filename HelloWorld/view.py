# -*-coding:utf-8-*-
# !/usr/bin/env python
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
from TestModel.models import Book, BookCategory, Chapter, SearchHistory, BookSheet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import pymysql
from django.forms.models import model_to_dict
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
import os
from HelloWorld.settings import STATIC_ROOT


@csrf_exempt
def hello(request):
    # context = {}
    # context['hello'] = 'hello world'
    # print(request)
    os.system('cd /home/HelloWorld')
    os.system('git checkout .')
    os.system('git pull')
    # os.system('sudo killall -9 uwsgi')
    # os.system('sudo uwsgi uwsgi.ini')
    # os.system('nginx -s reload')
    return HttpResponse('success')


def testGouzi(request):
    return HttpResponse('我是一个小毛贼,天天傻开心')


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


# 获取书籍列表
@csrf_exempt
def bookList(request):
    print(request)
    # 获取请求页数
    page = request.GET.get('page', 1)
    page = int(page)
    size = int(request.GET.get('size', 10))
    category = request.GET.get('category', '1')
    keywords = request.GET.get('keywords', '')

    # 保存记录到搜索历史
    # 查询所有书籍列表
    booklist = Book.objects.all()
    booklist = Book.filterBooks(booklist, request)
    # 生成分页器
    paginate = Paginator(booklist, size)
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
        print(p, '++++=======')
        # p.downloadurl = 'http://ebooktest:8000/ebooks/%s/%s.txt' % p.name % p.name
        # print(p['downloadurl'],'----------------')
        b = model_to_dict(p)
        L.append(b)

    if keywords:
        listCount = len(L)
        haveInsert = 0
        if listCount != 0:
            haveInsert = 1

        try:
            searchObj = SearchHistory.objects.get(keyword=keywords)
            if searchObj:
                searchObj.count = searchObj.count + 1
                searchObj.haveInsert = haveInsert
                searchObj.save()
                print(searchObj)
        except SearchHistory.DoesNotExist as e:
            searchObj = SearchHistory(keyword=keywords)
            searchObj.haveInsert = haveInsert
            searchObj.save()
    dict['code'] = '1'
    dict['message'] = '请求成功'
    dict['result'] = L
    return HttpResponse(json.dumps(dict, ensure_ascii=False, cls=DateEncoder))


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
    print(request.Get.get('id'))
    return HttpResponse('hehe')


@csrf_exempt
def sheetUpdate(request):
    sheetsJson = request.GET.get('content')
    sheets = json.loads(sheetsJson).get('sheets')
    books = Book.objects.all()
    List = []
    result = books.filter(id__in=sheets)
    ids = ''
    names = ''
    for obj in result:
        model = model_to_dict(obj)
        ids = ids + str(model.get('id')) + ','
        names = names + model.get('name') + ','
        List.append(model)
    # 存到书架对象上
    booksheet = BookSheet(bookids=ids, bookNames=names)
    booksheet.save()

    dict = {}
    dict['code'] = '1'
    dict['message'] = '请求成功'
    dict['result'] = List
    print(json.dumps(dict, ensure_ascii=False, cls=DateEncoder))
    return HttpResponse(json.dumps(dict, ensure_ascii=False, cls=DateEncoder))


@csrf_exempt
def readBook(request):
    chaptList = Chapter.objects.all()
    chaptList = Chapter.filterChapters(chaptList, request)
    dict = {}
    L = []
    bookid = request.GET.get('bookId', 3978)
    chaptid = request.GET.get('chapterId', 0)
    for p in chaptList:
        b = model_to_dict(p)

        bookname = ''
        BookList = Book.objects.all()
        BookList = BookList.filter(id=int(bookid))
        for obj in BookList:
            bookname = obj.name
        print(bookname)

        fileDirectpath = os.path.join(STATIC_ROOT, 'ebooks')
        fileDirectpath = os.path.join(fileDirectpath, bookname)
        fileDirectpath = os.path.join(fileDirectpath, bookname)
        fileDirectpath = os.path.join(fileDirectpath, '%s.txt' % b.get('chaperIdx'))
        print(fileDirectpath)
        content = ''
        with open(fileDirectpath, 'r') as f:
            content = f.read()
        b['content'] = content
        L.append(b)
    dict['code'] = '1'
    dict['message'] = '请求成功'
    dict['result'] = L
    return HttpResponse(json.dumps(dict, ensure_ascii=False))


@csrf_exempt
def chapters(request):
    chaptList = Chapter.objects.all()
    chaptList = Chapter.filterAllChapters(chaptList, request)
    dict = {}
    L = []
    for p in chaptList:
        b = model_to_dict(p)
        del b['id']
        del b['path']
        L.append(b)
    dict['code'] = '1'
    dict['message'] = '请求成功'
    dict['result'] = L
    return HttpResponse(json.dumps(dict, ensure_ascii=False))
    # 从章节列表中获取


def home(request):
    return render(request, 'index.html')
