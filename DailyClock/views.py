from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from DailyClock.models import Profile
from DailyClock.models import ProfileForm
from DailyClock.models import Result
from django.forms.models import model_to_dict
from HelloWorld import settings
from DailyClock.models import DKFeedBack
from DailyClock.models import DKVersionHistory
from  DailyClock.models import *
from TYMetro.models import UserProfile
from django.contrib.auth import authenticate, login
import datetime
from logging import getLogger
from django.shortcuts import render
import os
import json
from TestModel.models import models
from DailyClock.Apple.AppleLogin import decode_jwt
from DailyClock.JPush.TYJPush import get_phone_number
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.fields.files import FieldFile

logger = getLogger('HelloWorld')
class DateEncoders(json.JSONEncoder):
    def default(self, obj):
        print('obj11111')
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, FieldFile):
            try:
                if obj.url:
                    return obj.url
            except Exception as e:
                return ''
        else:
            return json.JSONEncoder.default(self, obj)


@csrf_exempt
def feedBack(request):
    # 请求方式
    method = request.method
    if method == 'POST':
        # 获取请求参数
        print('====================')
        print(request.body)
        body = json.loads(request.body, strict=False)
        assert isinstance(body, object)
        title = body["title"]
        content = body['content']
        phone = body['phone']
        strImg = body.get('imgs')
        FeedBack = DKFeedBack(title=title, content=content, phone=phone)
        FeedBack.save()
        if strImg:
            imgs = strImg.split(',')
            for img in imgs:
                profile = Profile.objects.get(url=img)
                if profile:
                    profile.url = img
                    print(profile, '0000000000000000000000000000')
                else:
                    profile = Profile()
                    profile.url = img
                    print(profile, '111111')
                profile.feedBackInfo = FeedBack
                profile.save()
        FeedBack.save()
        result = Result()
        jsonResult = model_to_dict(result)
        del jsonResult['id']
        data = json.dumps(jsonResult)
        return HttpResponse(data)
    else:
        feedBacks = DKFeedBack.objects.all()
        arr = []
        for feed in feedBacks:
            item = model_to_dict(feed)
            del item['id']
            arr.append(item)
        result = Result()
        dic = model_to_dict(result)

        del dic['id']
        dic['data'] = arr[::-1]
        return HttpResponse(json.dumps(dic, cls=DateEncoders))


@csrf_exempt
def versionHistory(request):
    versions = DKVersionHistory.objects.all()
    result = Result()

    dic = model_to_dict(result)
    del dic['id']
    arr = []
    for obj in versions:
        arr.append(model_to_dict(obj))
    dic['data'] = arr[::-1]
    return HttpResponse(json.dumps(dic, cls=DateEncoders))

@csrf_exempt
def fonts(request):
    all_fonts = DKFonts.objects.all()
    result = Result()

    dic = model_to_dict(result)
    del dic['id']
    arr = []
    for obj in all_fonts:
        arr.append(model_to_dict(obj))
    dic['data'] = arr[::-1]
    print(dic)
    return HttpResponse(json.dumps(dic, cls=DateEncoders))


@csrf_exempt
def index(request):
    context = {}
    # 获取上传图片的表单，并加到 context 中，使得该表达能在前端展示
    form = ProfileForm
    context['form'] = form
    return render(request, 'index.html', context)


@csrf_exempt
def save_profile(request):
    if request.method == "POST":
        # 接收 post 方法传回后端的数据
        MyProfileForm = ProfileForm(request.POST, request.FILES)
        print('-------')
        print(MyProfileForm)
        # 检验表单是否通过校验
        if MyProfileForm.is_valid():
            # 构造一个 Profile 实例
            profile = Profile()
            # 获取name
            profile.name = MyProfileForm.cleaned_data["name"]
            # 获取图片
            profile.picture = MyProfileForm.cleaned_data["picture"]

            # 保存
            profile.save()

            result = Result()
            dic = model_to_dict(result)
            del dic['id']

            # 拼接域名
            HOST = 'http://chengyan.shop/media/'
            if settings.DEBUG:
                HOST = 'http://0.0.0.0:8000/media/'

            profile.url = HOST + profile.picture.name
            profile.save()

            dic["data"] = profile.url
            retureData = json.dumps(dic)
            print(retureData)

            return HttpResponse(retureData)


        else:
            return redirect(to='index')

        return redirect(to='index')

@csrf_exempt
def today_card(request):
    # 获取数据库中最后一条数据
    result = DKJiTang.objects.all().order_by('-id')[:1]
    Res = Result()
    dic = model_to_dict(Res)
    del dic['id']
    data = []
    l = model_to_dict(result[0])
    del l['id']
    data.append(l)

    dic['data'] = data
    json_obj = json.dumps(dic,ensure_ascii=False,cls=DateEncoders)
    return HttpResponse(json_obj)


def private(request):
    return render(request, 'private.html')


def userProtocol(request):
    return render(request, 'userregiest.html')

def test(request):
    return render(request,'test.html')

def user_data(request,user):
    login(request, user)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    data = {'token': token}
    dic = model_to_dict(user)
    for key in dic:
        data.setdefault(key, dic[key])
    return JsonResponse({
        'code': 0,
        'message': '登录成功',
        'data': data
    })

def user_login(request):
    obj = json.loads(request.body)
    username = obj.get('phone', None)
    password = obj.get('password', None)
    type = obj.get('type',None)

    # 验证码登录
    if type == 'sms':
        try:
            user = authenticate(request, username=username)
            if user is None:
                user = UserProfile(mobile=username, username=username, nick_name=username)
                user.save()
                user = authenticate(request, username=username)
                return user_data(request, user)

            logger.info('---------')
            logger.info(user)
            logger.info('-----------')
            # user = UserProfile.objects.get(Q(mobile=username))
            return user_data(request, user)
        except Exception as e:
            user = UserProfile(mobile=username, username=username, nick_name=username)
            logger.info('===========')
            logger.info(model_to_dict(user))
            logger.info('=============')
            user.save()
            user = authenticate(request, username=username)
            return user_data(request,user)

    elif type == 'password':
        if username is None or password is None:
            return JsonResponse({'code': 500, 'message': '请求参数错误'})
        is_login = authenticate(request, username=username, password=password)
        if is_login is None:
            return JsonResponse({'code': 500, 'message': '账号或密码错误'})
        return user_data(request,is_login)
    elif type == 'apple':
        apple_token = obj.get('apple_token',None)
        tokens =  decode_jwt(apple_token)
        apple_id = tokens.get('sub',None)
        logger.info('--------')
        logger.info(tokens)
        logger.info('--------')
        logger.info('appleid:'+apple_id)
        try:
            user = UserProfile.objects.get(Q(apple_id=apple_id) & (~Q(mobile='')))
            logger.info('找到绑定的苹果用户:'+str(user))
            return user_data(request, user)
        except Exception as e:
            logger.info(e)
            logger.info('查询不到appleid绑定的手机号')
            try:
                user = UserProfile.objects.get(Q(apple_id=apple_id))
                logger.info('找到appleid用户:'+str(user))
                return user_data(request, user)
            except Exception as e:
                logger.error(e)
                logger.info('未发现appleid用户')
                user = UserProfile(apple_id=apple_id,username=apple_id)
                user.save()
                user = authenticate(request, username=apple_id)
                return user_data(request,user)
    elif type == 'onekey':
        login_token = obj.get('loginToken',None)
        phone = get_phone_number(login_token)
        logger.info("----------")
        logger.info(phone)
        logger.info("----------")
        try:
            user = authenticate(request, username=phone)
            if user is None:
                user = UserProfile(mobile=phone, username=phone, nick_name=phone)
                user.save()
                user = authenticate(request, username=phone)
                return user_data(request, user)
            return user_data(request,user)
        except Exception as e:
            user = UserProfile(mobile=phone, username=phone, nick_name=phone)
            logger.info('===========')
            logger.info(model_to_dict(user))
            logger.info('=============')
            user.save()
            user = authenticate(request, username=phone)
            return user_data(request,user)

