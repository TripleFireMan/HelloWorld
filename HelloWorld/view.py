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
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
import requests
import urllib
from  HelloWorld import qiniuuploader
from HelloWorld.buglyReporter import buglyReporter
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
#
# #开启定时工作
# try:
#     # 实例化调度器
#     scheduler = BackgroundScheduler()
#     DjangoJobStore().remove_all_jobs()
#     print(scheduler.get_jobs())
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     # 设置定时任务，选择方式为interval，时间间隔为10s
#     # 另一种方式为每天固定时间执行任务，对应代码为：
#     # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
#     @register_job(scheduler,"interval", seconds=10)
#     def my_job_jitang():
#         # 这里写你要执行的任务
#         do_work()
#     scheduler.start()
# except Exception as e:
#     print(e)
#     # 有错误就停止定时器
#     # scheduler.shutdown()


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

def print_helloworld():
    print('hello world')


# @csrf_exempt
def buglyReport(request):
    obj = request.body
    json_data = json.loads(obj)
    result = pic(json_data)
    params = {}
    infos = json_data['eventContent']
    params['title'] = infos['date'] + infos['appName'] + 'bugly统计日报'
    params['appName'] = infos['appName']
    params['crash'] = result['crash']
    params['url'] = infos['appUrl']
    params['pic'] = result['pic']
    params['version'] = result['version']
    print(params)
    json_data = dingTalk(params)
    return HttpResponse(json_data)

def dingTalk(params):
    title = params['title']
    subtitle = '线上最新版{0}-{1}crash率为{2}'.format(params['appName'],params['version'], params['crash'])
    headers={
        "Content-Type": "application/json"
            }
    data={
        "msgtype": "markdown",
        "markdown": {
            "title": '##{0}'.format(title),
            "text": "### {0}\n".format(title) +
                    "> {0}\n\n".format(subtitle) +
                    "> ![screenshot]({0})\n".format(params['pic']) +
                    "> ###### {0}-{1} [查看详情]({2}) \n".format(params['appName'],params['version'], params['url'])
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": False
        }
        }
    json_data=json.dumps(data)

    print(json_data)
    requests.post(url='https://oapi.dingtalk.com/robot/send?access_token=5f43f46a899baf1e16b711a040e775a3237a3a30f044b313bb9b1d6ac2fb4542',data=json_data,headers=headers)

    return json_data

def pic(params):
    print('11')
    tab = PrettyTable()

    content_event=  params['eventContent']
    data = content_event['datas']
    app_name = content_event['appName']
    result = {}
    # 设置表头
    tab.field_names = ["app名称", "版本号", "联网用户数", "影响用户数", "crash次数", "crash率"]
    for index in range(0,len(data)):
        app_version = data[index]['version']
        app_version = urllib.parse.unquote(app_version)
        crash_user = data[index]['crashUser']
        access_user = data[index]['accessUser']
        crash_count = data[index]['crashCount']
        crash_lv = "%.2f"%(crash_user * 100.0/access_user) + "%"
        tab.add_row([app_name,app_version,access_user,crash_user,crash_count,crash_lv])
        if  index == len(data)-1:
            latest_crash_lv = crash_lv
            result['crash'] = latest_crash_lv

            result['version'] = app_version
    # 表格内容插入
    tab_info = str(tab)
    space = 7
    file_path_url = os.path.abspath('')
    # PIL模块中，确定写入到图片中的文本字体
    font = ImageFont.truetype('{0}/collect_static/uploads/楷体_GB2312.ttf'.format(file_path_url), 30, encoding='utf-8')
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (255, 255,255, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space, space), unicode(tab_info, 'utf-8'), fill=(255, 255, 255), font=font)
    # python3
    draw.multiline_text((space,space), tab_info, fill=(0,0,0), font=font)
    file_path = os.path.join('{0}/collect_static/uploads/12345.png'.format(file_path_url))
    im_new.save(file_path)

    del draw
    try:
        res = qiniuuploader.qiniu_upload(file_path)
        result['pic'] = res
    except Exception as e:
        print(e)
    return result