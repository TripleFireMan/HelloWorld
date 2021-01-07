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

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.forms.models import model_to_dict
from TYMetro.Apple.AppleLogin import decode_jwt
from TYMetro.JPush.TYJPush import get_phone_number

logger = getLogger('HelloWorld')

class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(mobile=username))  # 输入username和mobile都能查询到用户
            logger.info(user)
            return user

            # if user.password == password:  # 校验密码
            #     return user
        except Exception as e:
            return None

def log110(request):
    return  HttpResponse('110')

def get_phone(request):
    token = request.POST.get('token')
    result = get_phone_number(token)
    return HttpResponse(result)

def user_login(request):
    obj = json.loads(request.body)
    username = obj.get('phone', None)
    password = obj.get('password', None)
    type = obj.get('type',None)

    # 验证码登录
    if type == 'sms':
        try:
            user = authenticate(request, username=username)
            logger.info('---------')
            logger.info(user)
            logger.info('-----------')
            # user = UserProfile.objects.get(Q(mobile=username))
            return user_data(request, user)
        except Exception as e:
            user = UserProfile(mobile=username)
            user.save()
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
                logger.info('未发现appleid用户')
                user = UserProfile(apple_id=apple_id)
                user.save()
                return user_data(request,user)
    elif type == 'onekey':
        login_token = obj.get('loginToken',None)
        phone = get_phone_number(login_token)
        try:
            user = authenticate(request, username=phone)
            logger.info('1111111111')
            logger.info(user.mobile)
            logger.info('2222222222')
            return user_data(request,user)
        except Exception as e:
            user = UserProfile(mobile=phone)

            logger.info('===========')
            logger.info(model_to_dict(user))
            logger.info('=============')

            user.save()
            user = authenticate(request, username=phone)
            return user_data(request,user)


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

# @api_view(['POST','GET'])
def bindUser(request):
    user = UserProfile()
    body = request.body
    params = json.loads(body)

    logger.info(params)

    source= params['source']
    mobile = params['mobile']
    apple_id = params['apple_id']

    try:
        user = UserProfile.objects.get(Q(apple_id=apple_id))
    except Exception as e:
        pass

    if source == 'apple':
        try:
            mobileUser = UserProfile.objects.get(Q(mobile=mobile))
            mobileUser.apple_id = user.apple_id
            mobileUser.save()
            logger.info('找到对应用户，并将apple_id绑定上去了')
            logger.info('删除旧的')
            isDelete =  user.delete()
            logger.info(isDelete)

            return user_data(request,mobileUser)
        except Exception as e:
            user.mobile = mobile
            user.save()
            logger.info('没找到对应用户，直接绑定手机号成功')
            return user_data(request,user)




# 下面的3个装饰器，全部来自from引用
# 相当与给接口增加了用户权限校验和token校验
@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def get_info(request):
    data = 'some info'
    user = request.user
    logger.info('=================')
    logger.info(model_to_dict(user))
    return JsonResponse(
        {
            'code': 200,
            'message': '请求成功',
            'data': data
        }
    )

# @api_view(['POST','GET'])
# @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))
def modifierUser(request):
    body = json.loads(request.body)
    logger.info(body)
    nickname = body.get('nickname','')
    sex = body.get('sex','')
    birthday = body.get('birthday','')
    avator = body.get('avator','')
    intruduce = body.get('introduce','')
    user = request.user
    user.nick_name = nickname
    user.gender = sex
    user.birthday = birthday
    user.img = avator
    user.introduce = intruduce
    user.save()

    logger.info('=================')
    logger.info(model_to_dict(user))

    return user_data(request,user)

    # return JsonResponse(
    #     {
    #         'code': 200,
    #         'message': '请求成功',
    #         'data': data
    #     }
    # )