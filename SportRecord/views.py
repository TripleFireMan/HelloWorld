#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:24 下午
# @Author  : chengyan
# @File    : urls.py
# @Software: macos
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def getUsers(request):
        return HttpResponse('123')
    