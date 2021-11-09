from django.shortcuts import render

# Create your views here.
from django.forms.models import model_to_dict
from django.http import HttpResponse
from ZhuaZhou.models import ZhuaZhouModel,Carousel
from DailyClock.models import Result
import json
import datetime
from easy_thumbnails.files import get_thumbnailer
from rest_framework.decorators import api_view

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

@api_view(['get'])
def homePageInfo(request):
    # 请求性别参数
    requestGender = request.GET.get('gender')
    versions = ZhuaZhouModel.objects.all()
    carousel = Carousel.objects.all()
    result = Result()
    gender = request.GET.get('gender')
    if gender == None:
        pass
    elif gender == '男':
        versions = versions.filter(gender='男')
    else:
        versions = versions.filter(gender='女')
    dic = model_to_dict(result)
    del dic['id']
    arr = []
    carousel_return = []
    for obj in versions:
        path = get_thumbnailer(obj.img, relative_name='product_image')
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
    for obj in carousel:
        path = get_thumbnailer(obj.img)
        url = path.file.url
        r_dic = model_to_dict(obj)
        r_dic.pop('id')
        r_dic.pop('img')
        r_dic['url'] = url
        carousel_return.append(r_dic)
    data = {}
    data['props'] = arr
    data['carousel'] = carousel_return
    # 默认文案展示
    playDesIntroduce = '''1. 点击下方‘开始’按钮，道具开始轮播，再次点击抓按钮，道具停止轮播，宝宝抓到的道具即为抓周
2. 抓周结束之后，再弹框内部点击制作抓周证，将跳转到抓周证制作页面
3. 填写抓周证资料，保存之后，即可分享到朋友圈'''
    data['introduce'] = playDesIntroduce
    dic['data'] = data
    return HttpResponse(json.dumps(dic,cls = DateEncoders))
