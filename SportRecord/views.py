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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters,viewsets,status
from rest_framework.pagination import PageNumberPagination
from .Mixin import SportRecordResponseMixin
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView



from django.core.paginator import Paginator
logger = getLogger('HelloWorld')

def get_uid_from_headers(request):
    userInfo = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
    return userInfo['user_id']

def buildTreeMenu(menuLst):
        resultMenuLst: list[SRMenu] = list()
        for menu in  menuLst:
            # 寻找子节点
            # 判断父节点，添加到集合
            for e in menuLst:
                if not hasattr(menu,'children'):
                    menu.children = list()
                if e.parent_id == menu.id:
                    menu.children.append(e)
            if menu.parent_id == 0:
                resultMenuLst.append(menu)
        return resultMenuLst

# 分页控制器
class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'pageSize'
    page_query_param = 'pageNum'

    def get_paginated_response(self, data):
        return {
            "currentPage":self.page.number,
            "list":data,
            "totle":self.page.paginator.count
        }

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
    
    def post(self, request):
        username = request.GET.get('username')
        pwd = request.GET.get('password')
        try:
            user = SRUserProfile.objects.get(username = username, password = pwd)
            token = self.gettoken(request=request)
            logger.info(f'{user.name}登录成功,{datetime.now()}')
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
                for menu in menuList:
                    menuSet.add(menu)
            menuLst = list(menuSet)
            sortedMenuLst = sorted(menuLst)
            menuLst = buildTreeMenu(sortedMenuLst)
            serializersMenuLst = list()
            for obj in menuLst:
                serializersMenuLst.append(SRMenuSerializer(obj).data)
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
        propertys = [SRPropertySerializier(obj).data for obj in SRProperty.objects.all() ] 
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
    
class SRUserViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    queryset = SRUserProfile.objects.all()
    serializer_class = SRUserProfileSerializer

    @action(detail=False, methods=['DELETE'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('idList', [])
        if not ids:
            return Response({'error': '未提供删除ID列表'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():  # 事务保证原子性
                self.queryset.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['PATCH'], url_path='update-pwd')
    def update_pwd(self, request,*args, **kwargs):
        sourcePwd = request.data.get('sourcePwd', '')
        newPwd = request.data.get('newPwd', '')
        user = self.queryset.get(id = self.kwargs['pk'])
        if sourcePwd != user.password:
            return Response({'error': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():  # 事务保证原子性
                user.password = newPwd
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    @action(detail=True, methods=['POST'], url_path='grant-role')
    def grant_role(self, request, *args, **kwargs):
        rolelist = request.data.get('roleList')
        user = self.queryset.get(id = self.kwargs['pk'])
        roles = SRRole.objects.filter(id__in = rolelist)
        for role in user.role.all():
            user.role.remove(role)
        for newRole in roles:
            user.role.add(newRole)
        user.save()
        return JsonResponse({'code':200,'message':'请求成功'})
        
class RoleViewSet(SportRecordResponseMixin, viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRRoleSerializer
    queryset = SRRole.objects.all()
    @action(detail=False, methods=['DELETE'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('idList', [])
        if not ids:
            return Response({'error': '未提供删除ID列表'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():  # 事务保证原子性
                self.queryset.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
    

class PhotoViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    serializer_class = SRPhotoSerializer
    queryset = SRPhoto.objects.all()
    

class MenuListView(View):
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
        menuLst = buildTreeMenu(sortedMenuLst)
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

            # 超级管理员自动添加对应的菜单
            superRole = SRRole.objects.get(id=33)
            superRole.menu.add(menu)
            superRole.save()
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

class PropertyViewSet(SportRecordResponseMixin, viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRPropertySerializier
    queryset = SRProperty.objects.all()


class ClothingViewSet(SportRecordResponseMixin, viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRClothingSerializer
    queryset = SRClothing.objects.all()

    
# 运动记录
class SportRecordViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRUserSportRecordSerializer
    queryset = SRUserSportRecord.objects.all()
# 心情 
class MoodViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRMoodSerializer
    queryset = SRMood.objects.all()
# 伴侣
class PartnerViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRPartnerSerializer
    queryset = SRPartner.objects.all()

    def create(self, request, *args, **kwargs):
        # 添加自定义逻辑（如注入当前用户ID）
        serializer = self.get_serializer(data=request.data)
        sruser = SRUserProfile.objects.get(id=request.data.get('uid'))
        serializer.is_valid(raise_exception=True)
        serializer.save(creater=sruser)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['DELETE'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('idList', [])
        if not ids:
            return Response({'error': '未提供删除ID列表'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():  # 事务保证原子性
                self.queryset.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UserPartnerViewSet(SportRecordResponseMixin,GenericViewSet,ListModelMixin,CreateModelMixin):
    serializer_class = SRPartnerSerializer

    # 查询用户的伴侣
    def get_queryset(self):
        uid = self.kwargs.get('uid')
        try:
            user = SRUserProfile.objects.get(id=uid)
            return user.partners.all()
        except:
            return ()

    # 支持用户创建伴侣
    def perform_create(self, serializer):
        user = get_object_or_404(SRUserProfile, pk=self.kwargs['uid'])
        partner = serializer.save()
        user.partners.add(partner)  # 自动关联用户与角色‌
        
class PlaceViewSet(SportRecordResponseMixin,viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = SRPlaceSerializer
    queryset = SRPlace.objects.all()

class UserPlaceViewSet(SportRecordResponseMixin,GenericViewSet,ListModelMixin,CreateModelMixin):
    serializer_class = SRPlaceSerializer

    # 查询用户地址
    def get_queryset(self):
        uid = self.kwargs.get('uid')
        defaultplaces = SRPlace.objects.filter(type = '1')
        try:
            user = SRUserProfile.objects.get(id=uid)
            return defaultplaces.all().union(user.places.all())
        except:
            return ()
    # 支持用户创建地址
    def perform_create(self, serializer):
        user = get_object_or_404(SRUserProfile, pk=self.kwargs['uid'])
        place = serializer.save()
        user.places.add(place)  # 自动关联用户与角色‌
    