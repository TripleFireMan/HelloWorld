from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def feedBack(request):

    return HttpResponse('222')

def versionHistory(request):
    return HttpResponse('334333')