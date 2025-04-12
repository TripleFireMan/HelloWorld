#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:24 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views import View
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.db.models import F,Value,CharField
from django.db.models.functions import Concat
import json
from SportRecord.models import *
from rest_framework_jwt.settings import api_settings
from logging import getLogger
from datetime import datetime
from rest_framework_jwt.utils import jwt_decode_handler
from django.core.paginator import Paginator
logger = getLogger('HelloWorld')

def defaultErrorDic(msg):
    return {'code':201, 'message':msg}

def get_uid_from_headers(request):
    userInfo = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
    return userInfo['user_id']

# 校验必须有token的情况
def CommonHandle(func):
    def warp(obj,request,*args, **kwargs):
        try:
            uid = get_uid_from_headers(request)
            if uid != '':
                kwargs['uid'] = uid
                if len(request.GET) != 0:
                    kwargs.update(request.GET.dict())
                return func(obj,request,*args, **kwargs)
        except Exception as e:
            logger.error(f'{e}')
            return JsonResponse({'code':201,'message':f'{e}'})
    return warp

# Create your views here.
class TextView(View):
    def get(self, request):
        user = SRUserProfile.objects.get(mobile='18612545535')
        jwt_payload_hander =  api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_hander = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_hander(user)
        token =  jwt_encode_hander(payload)

        return JsonResponse({'code':200,'token':token})
    
class LoginView(View):

    def gettoken(self,request):
        username = request.GET.get('username')
        user = SRUserProfile.objects.get(username=username)
        try:
            jwt_payload_hander =  api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_hander = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_hander(user)
            token =  jwt_encode_hander(payload)
            return token
        except Exception as e:
            return ''
    
    def buildTreeMenu(self,menuLst):
        resultMenuLst: list[SRMenu] = list()
        for menu in  menuLst:
            # 寻找子节点
            # 判断父节点，添加到集合
            for e in menuLst:
                if not hasattr(menu,'children'):
                    logger.info('动态添加子节点0')
                    menu.children = list()
                if e.parent_id == menu.id:
                    logger.info('动态添加子节点1')
                    menu.children.append(e)
            if menu.parent_id == 0:
                resultMenuLst.append(menu)
        return resultMenuLst
    
    def post(self, request):
        username = request.GET.get('username')
        pwd = request.GET.get('password')
        try:
            user = SRUserProfile.objects.get(username = username, password = pwd)
            token = self.gettoken(request=request)
            logger.error(user)
            sruser = SRUserProfileSerializer(user).data
            if token != '':
                sruser['token'] = token

            # roleList = SRRole.objects.raw("SELECT id , name FROM SportRecord_srrole WHERE id in (SELECT srrole_id FROM SportRecord_sruserprofile_role WHERE sruserprofile_id = "+str(user.id) +")")
            roleList = user.role.all()
            # roleDicList = []
            menuSet:set[SRMenu] = set()
            for obj in roleList:
                # role = {}
                # role['name'] = obj.name
                menuList = obj.menu.all()
                logger.info(menuList)
                for menu in menuList:
                    menuSet.add(menu)
            menuLst = list(menuSet)
            sortedMenuLst = sorted(menuLst)
            menuLst = self.buildTreeMenu(sortedMenuLst)
            logger.info('菜单列表')
            logger.info(menuLst)
            serializersMenuLst = list()
            for obj in menuLst:
                serializersMenuLst.append(SRMenuSerializer(obj).data)
            logger.info(menuLst)
            sruser["menuList"] = serializersMenuLst
            # sruser['role'] = roleDicList

            return JsonResponse({'code':200,'message':'请求成功','data':sruser})
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':201,'message':'密码或用户名错误','data':{
                'username':username,
                'pwd':pwd
            }})
        

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # uid = request.GET.get('uid')
        result = {}
        result['code'] = 200
        result['message'] = '请求成功'
        # result['uid'] = uid
        # result['args'] = args
        # result['kwargs'] = request.GET
        data = {}
        # 查询道具信息
        propertys = SRProperty.objects.values('name','icon','bgColor')
        data['propertys'] = list(propertys)
        # 查询分类信息
        categorys = SRSportCategory.objects.values('name','icon')
        data['categorys'] = list(categorys)
        result['data'] = data
        
        return HttpResponse(json.dumps(result))

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')


class ConfigView(View):
    def get(self, request, *args, **kwargs):
        
        result = {}
        result['code'] = 200
        result['message'] = '请求成功'
    
        data = {}
        # 查询道具信息
        propertys = [{**model_to_dict(obj,exclude=['icon']),'icon':SR_BASE_URL_MEDIA_PATH + obj.icon.url} for obj in SRProperty.objects.all() ] 
        data['propertys'] = list(propertys)
        # 查询分类信息
        categorys = [{**obj,'icon':SR_BASE_URL_MEDIA_PATH + obj['icon']} for obj in SRSportCategory.objects.values('name','icon')] 
        data['categorys'] = list(categorys)
        # 服装
        clothings = SRClothing.objects.annotate(
             newIcon = Concat(
                  Value(SR_BASE_URL_MEDIA_PATH),
                  F('icon'),
                  output_field=CharField()
                  )
        ).values('id','newIcon','name')
        data['clothings'] = list(clothings)
        # 心情
        mood = [{**obj,'icon':f'{SR_BASE_URL_MEDIA_PATH}'+obj['icon']} for obj in SRMood.objects.values('id','icon','name')]
        data['moods'] = list(mood)
        # 评分
        scores = [{**obj,'icon':f'{SR_BASE_URL_MEDIA_PATH}'+obj['icon'],'score':obj['score']} for obj in SRScore.objects.values('id','icon','name','score')]
        data['scores'] = list(scores)
        # 查询系统配置
        config = SRSystemConfig.objects.get(name='运动记录')
        config_dic = model_to_dict(config)
        del config_dic['id']
        data['config'] = config_dic
        result['data'] = data
        
        return HttpResponse(json.dumps(result))

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
class SaveView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')
    @CommonHandle
    def post(self, request, *args, **kwargs):
        # 获取修改的用户id，如果没有传递的话，认为是修改自己的用户信息
        uid = kwargs.get('userid')
        if uid is None:
            uid = kwargs.get('uid')
        # 如果不存在uid或者uid为-1，认为是新增
        if uid is None or uid == '-1':
            logger.info('即将添加数据1')
            user = SRUserProfile(username=kwargs.get('username'),
                                 address=kwargs.get('address'),
                                 status=False if kwargs.get('status') == '0' else True,
                                 remark = kwargs.get('remark'),
                                 mobile=kwargs.get('mobile'),
                                 password='123456',
                                 gender='女' if kwargs.get('gender') == '2' else "男"
                                 )
            user.save()
            return JsonResponse({'code':200,'message':'请求成功','data':SRUserProfileSerializer(user).data})
            
        else:
            SRUserProfile.objects.filter(id=uid).update(
                                 mobile=kwargs.get('mobile'),
                                 address=kwargs.get('address'),
                                 status = False if kwargs.get('status') == '0' else True,
                                 remark=kwargs.get('remark'),
                                 gender='女' if kwargs.get('gender') == '2' else "男") 
        return JsonResponse({'code':200,'message':'请求成功','data':SRUserProfileSerializer(SRUserProfile.objects.get(id=uid)).data})
    
    @CommonHandle
    def delete(self,request, *args, **kwargs):
        uid = kwargs['userid']
        SRUserProfile.objects.get(id = uid).delete()
        return JsonResponse({'code':200,'message':'删除成功'})

class PwdView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')

    def post(self, request, *args, **kwargs):
        uid = get_uid_from_headers(request)
        oldPwd = request.GET.get('sourcePwd')
        newPwd = request.GET.get('newPwd')
        if uid != '':
            try:
                user = SRUserProfile.objects.get(id = uid)
                if oldPwd == user.password:
                    user.password = newPwd
                    user.updated = datetime.now()
                    user.save()
                    return JsonResponse({'code':200,'message':'修改成功，下次登录使用新密码'})
                else:
                    return JsonResponse({'code':201,'message':'密码错误'})
            except:
                return JsonResponse({'code':201,'message':'密码错误'})
            
class ResetPwdView(View):
    @CommonHandle
    def post(self, request, *args, **kwargs):
        uid = kwargs.get('userid')
        user = SRUserProfile.objects.get(id = uid)
        user.password = '123456'
        user.save()
        return JsonResponse({'code':200,'message':'重置成功'})
    
class AvatorView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')
    
    @CommonHandle
    def post(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        if kwargs.get('userid'):
            uid = kwargs.get('userid')
        user = SRUserProfile.objects.get(id = uid)
        user.avator = request.FILES['avator']
        user.save()
        return JsonResponse({'code':200,'message':'上传成功','data':{'url':user.avator.url}})
        
class SearchView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        uid = kwargs['uid']
        pageNum = kwargs['pageNum']
        pageSize = kwargs['pageSize']
        query = kwargs['query']
        result = Paginator(SRUserProfile.objects.filter(name__icontains=query),pageSize).page(pageNum)
        # result_list = result.object_list.values()
        count = SRUserProfile.objects.filter(name__icontains=query).count()
        return JsonResponse({'code':200,'message':'请求成功','data':{'list':list([SRUserProfileSerializer(user).data for user in result]),'totle':count,'curPageNo':pageNum,'pageSize':pageSize}})
    
    @CommonHandle
    def post(self, request, *args, **kwargs):
        logger.info(request)
        return JsonResponse(kwargs)
    
class ActionView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        user = SRUserProfile.objects.get(id=uid)
        return JsonResponse({'code':200, 'message':'请求成功','data':SRUserProfileSerializer(user).data})
    @CommonHandle
    def delete(self, request, *args, **kwargs):
        idList =  json.loads(kwargs.get('idList'))
        SRUserProfile.objects.filter(id__in = idList).delete()
        return JsonResponse({'code':200,'message':'删除成功'})
    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
class CheckView(View):
    @CommonHandle
    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if SRUserProfile.objects.filter(username = username).exists():
            return JsonResponse({'code':201,'message':'用户名已存在'})
        else:
            return JsonResponse({'code':200,'message':'请求成功'})

class RoleView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        rid = kwargs.get('id')
        role = SRRole.objects.get(id = rid)
        return JsonResponse({'code':200,'message':'请求成功','data':SRRoleSerializer(role).data})
    
    @CommonHandle
    def post(self, request, *args, **kwargs):
        rid = kwargs.get('rid')
        if rid is None or rid == '-1':
            role = SRRole(
                name = kwargs.get('name'),
                code = kwargs.get('code'),
                remark = kwargs.get('remark')
            )
            role.save()
            return JsonResponse({'code':200,'message':'添加成功','data':SRRoleSerializer(role).data})
        else:
            SRRole.objects.filter(id = rid).update(
                name = kwargs.get('name'),
                code = kwargs.get('code'),
                remark = kwargs.get('remark'),
                update_time = datetime.now()
            )
            return JsonResponse({'code':200,'message':'修改成功','data':SRRoleSerializer(SRRole.objects.get(id=rid)).data})
        

class RoleListView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        roleList = SRRole.objects.all()
        logger.info(roleList)
        return JsonResponse({'code':200,'data':{"list":[SRRoleSerializer(obj).data for obj in roleList]},'message':'请求成功'})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
    @CommonHandle
    def delete(self, request, *args, **kwargs):
        idLst = json.loads(kwargs.get('idList'))
        SRRole.objects.filter(id__in = idLst).delete()
        return JsonResponse({'code':200,'message':'删除成功'})
        
    
class RoleSearchView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        pageNum = kwargs.get('pageNum')
        pageSize = kwargs.get('pageSize')
        query = kwargs.get('query')
        roleList = Paginator(SRRole.objects.filter(name__icontains = query),pageSize).page(pageNum)
        count = SRRole.objects.filter(name__icontains = query).count()
        return JsonResponse({'code':200,'data':{"list":[SRRoleSerializer(obj).data for obj in roleList],'curPageNo':pageNum,'pageSize':pageSize,'totle':count},'message':'请求成功'})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
class GrantView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')
    
    @CommonHandle
    def post(self, request, *args, **kwargs):
        roleList =  json.loads(kwargs.get('roleList'))
        userid = kwargs.get('userid')
        user = SRUserProfile.objects.get(id = userid)
        roles = SRRole.objects.filter(id__in = roleList)
        for role in user.role.all():
            user.role.remove(role)
        for newRole in roles:
            user.role.add(newRole)
        user.save()
        return JsonResponse({'code':200,'message':'请求成功'})

class MenuListView(View):

    def buildTreeMenu(self,menuLst):
        resultMenuLst: list[SRMenu] = list()
        for menu in  menuLst:
            # 寻找子节点
            # 判断父节点，添加到集合
            for e in menuLst:
                if not hasattr(menu,'children'):
                    logger.info('动态添加子节点0')
                    menu.children = list()
                if e.parent_id == menu.id:
                    logger.info('动态添加子节点1')
                    menu.children.append(e)
            if menu.parent_id == 0:
                resultMenuLst.append(menu)
        return resultMenuLst

    @CommonHandle
    def get(self, request, *args, **kwargs):
        pageNum = kwargs.get('pageNum')
        pageSize = kwargs.get('pageSize')
        query = '' if kwargs.get('query') is None else kwargs.get('query')
        menuList = []
        if pageNum and pageSize and query:
            menuList = Paginator(SRMenu.objects.filter(name__icontains = query),pageSize).page(pageNum)
        else:
            menuList = SRMenu.objects.all()

        menuSet:set[SRMenu] = set()
        for menu in menuList:
            menuSet.add(menu)    
        menuLst = list(menuSet)
        sortedMenuLst = sorted(menuLst)
        menuLst = self.buildTreeMenu(sortedMenuLst)
        mlist = [SRMenuSerializer(l).data for l in menuLst]
        count = SRMenu.objects.filter(name__icontains = query).count()
        return JsonResponse({'code':200,'data':{"list":mlist,'curPageNo':pageNum,'pageSize':pageSize,'totle':count},'message':'请求成功'})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

class MenuView(View):
    @CommonHandle
    def get(self, request, *args, **kwargs):
        mid = kwargs.get('id')
        menu = SRMenu.objects.get(id = mid)
        return JsonResponse({'code':200,'data':SRMenuSerializer(menu).data,'message':'请求成功'})
    @CommonHandle
    def post(self, request, *args, **kwargs):
        mid = kwargs.get('id')
        m = {k:kwargs[k] for k in kwargs if k in ['name','parent_id','icon','order_num','path','remark','component','menu_type']}
        if mid == '-1':            
            logger.info(m)
            menu = SRMenu(
                 **m
            )
            menu.save()
            return JsonResponse({'code':200,'data':SRMenuSerializer(menu).data,'message':'请求成功'})
        else:
            SRMenu.objects.filter(id = mid).update(
                **m
            )
            return JsonResponse({'code':200,'data':SRMenuSerializer(SRMenu.objects.get(id=mid)).data,'message':'请求成功'})
    @CommonHandle
    def delete(self, request, *args, **kwargs): 
        logger.info(kwargs)
        mid = kwargs.get('id')
        menu = SRMenu.objects.get(id=mid)
        logger.info(SRMenuSerializer(menu).data)
        if menu.parent_id == 0 and SRMenu.objects.filter(parent_id = mid).count() > 0:
            return JsonResponse({'code':201,'message':'子节点不为空，不能删除'})
        
        for role in menu.roles.all():
            role.menu.remove(menu)
        menu.delete()
        return JsonResponse({'code':200,'message':'删除成功'})

class GrantMenuView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')
    @CommonHandle
    def post(self, request, *args, **kwargs):
        rid = kwargs.get('rid')
        idList = json.loads(kwargs.get('menuList'))
        role = SRRole.objects.get(id = rid)
        menus = SRMenu.objects.filter(id__in = idList)
        for menu in role.menu.all():
            role.menu.remove(menu)
        for newMenu in menus:
            role.menu.add(newMenu)
        role.save()
        return JsonResponse({'code':200,'message':'请求成功'})