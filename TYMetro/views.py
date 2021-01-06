from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from TYMetro.JPush.TYJPush import get_phone_number
from logging import getLogger
from TYMetro.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers import serialize

from django.forms.models import model_to_dict

logger = getLogger('HelloWorld')

def log110(request):
    return  HttpResponse('110')

def get_phone(request):
    token = request.POST.get('token')
    result = get_phone_number(token)
    return HttpResponse(result)

@csrf_exempt
def login(request):
    # 获取请求的参数
    logger.info(request.body)
    body = json.loads(request.body)
    type = body['type']
    if  type == 'sms':
        phone = body['phone']
        phone_user = UserProfile.objects.all().filter(mobile=phone)
        # 校验账号是否存在,如果不存在创建一个新账号
        if phone_user.count() == 0:
            new_user = UserProfile()
            new_user.mobile = phone
            new_user.save()
            # 封装数据
            result = {'code': 0,
                      'message': 'success'}
            result['data'] = model_to_dict(new_user)
            return JsonResponse(result,safe=False)
        else:
            # 封装数据
            result = {'code': 0,
                      'message': 'success'}

            # 返回用户的数据
            for info in phone_user:
                logger.info(info)
                dict = model_to_dict(info)
                logger.info(dict)
                result['data'] = dict
            return JsonResponse(result, safe=False)
    elif type == 'password':
        phone = body['phone']
        password = body['password']
        phone_user = UserProfile.objects.all().filter(mobile=phone)

        # 校验账号是否存在
        if phone_user.count() == 0:
            return JsonResponse(({'code':-1,'message':'该用户不存在','data':{}}))

        # 校验密码是否正确
        user =  phone_user.filter(password=password)
        logger.info(user)
        if user.count() == 0:
            return JsonResponse(({'code':-2,'message':'密码错误','data':{}}))

        # 封装数据
        result = {'code': 0,
                  'message': 'success'}

        # 返回用户的数据
        for info in user:
            logger.info(info)
            dict = model_to_dict(info)
            logger.info(dict)
            result['data'] = dict
        return JsonResponse(result, safe=False)

    elif type == 'onekey':
        pass
    elif type == 'apple':
        pass




    return HttpResponse()