from django.shortcuts import render

# Create your views here.
from django.forms.models import model_to_dict
from django.http import HttpResponse
from ZhuaZhou.models import ZhuaZhouModel
from DailyClock.models import Result
import json
import datetime
from easy_thumbnails.files import get_thumbnailer
from rest_framework.decorators import api_view
from easy_thumbnails.options import ThumbnailOptions
from HelloWorld.settings import MEDIA_URL
from filer.storage import PublicFileSystemStorage
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

class DateEncoders(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

@api_view(['GET'])
def tools(request):
    versions = ZhuaZhouModel.objects.all()
    print(versions)
    result = Result()
    gender = request.GET.get('gender')
    if  gender == None:
          pass
    elif  gender == '男':
        versions = versions.filter(gender = '男')
    else:
        versions = versions.filter(gender = '女')
    dic = model_to_dict(result)
    del dic['id']
    arr = []
    for obj in versions:
        path = get_thumbnailer(obj.img,relative_name='product_image')
        thumbnail_options = {'crop': True}
        # for size in (180, 360):
        #     thumbnail_options.update({'size': (size, size)})
        url = path.file.url
        small = path['small'].url
        big = path['big'].url
        r_dic = model_to_dict(obj)
        r_dic.pop('id')
        r_dic.pop('img')
        r_dic['url'] = url
        r_dic['bigUrl'] = big
        r_dic['smallUrl'] = small
        arr.append(r_dic)
    dic['data'] = arr
    return HttpResponse(json.dumps(dic, cls=DateEncoders))

# #开启定时工作
#
# try:
#     # 实例化调度器
#     scheduler = BackgroundScheduler()
#     # 调度器使用DjangoJobStore()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     # 设置定时任务，选择方式为interval，时间间隔为10s
#     # 另一种方式为每天固定时间执行任务，对应代码为：
#     # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
#     @register_job(scheduler,"interval", seconds=10)
#     def my_job1():
#         # 这里写你要执行的任务
#         print('250')
#     register_events(scheduler)
#     scheduler.start()
# except Exception as e:
#     print(e)
#     # 有错误就停止定时器
#     scheduler.shutdown()
