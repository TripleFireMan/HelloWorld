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
import datetime
from django.shortcuts import render

import json


class DateEncoders(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
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
        result = Result()
        result.status = 1001
        result.message = '不支持get请求'
        return HttpResponse(json.dumps(model_to_dict(result)))


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
            HOST = 'http://chengyan.shop/static/'
            if settings.DEBUG:
                HOST = 'http://0.0.0.0:8000/static/'

            profile.url = HOST + profile.picture.name
            profile.save()

            dic["data"] = profile.url
            retureData = json.dumps(dic)
            print(retureData)

            return HttpResponse(retureData)


        else:
            return redirect(to='index')

        return redirect(to='index')


def private(request):
    return render(request, 'private.html')


def userProtocol(request):
    return render(request, 'userregiest.html')
