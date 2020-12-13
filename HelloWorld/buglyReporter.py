#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/13 10:54 下午
# @Author  : chengyan
# @File    : buglyReporter.py
# @Software: macos

import sqlite3
import os
from TestModel.models import BuglyData
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
from HelloWorld import qiniuuploader
import urllib
import json

class buglyReporter(object):

    # def __init__(self,version,appname,text):
    #     self.version = version
    #     self.appName = appname
    #     self.text = text
    #     print(self.text)
    # def __str__(self):
    #     return self.version + ' ' + self.appName + ' ' + self.text


    # def insert_tbl(self,jsondata):

    def pic(self,params):
        print('11')
        tab = PrettyTable()

        content_event = params['eventContent']
        data = content_event['datas']
        app_name = content_event['appName']
        result = {}
        # 设置表头
        tab.field_names = ["app名称", "版本号", "联网用户数", "影响用户数", "crash次数", "crash率"]
        for index in range(0, len(data)):
            app_version = data[index]['version']
            app_version = urllib.parse.unquote(app_version)
            crash_user = data[index]['crashUser']
            access_user = data[index]['accessUser']
            crash_count = data[index]['crashCount']
            crash_lv = "%.2f" % (crash_user * 100.0 / access_user) + "%"
            tab.add_row([app_name, app_version, access_user, crash_user, crash_count, crash_lv])
            if index == len(data) - 1:
                latest_crash_lv = crash_lv
                result['crash'] = latest_crash_lv

                result['version'] = app_version
        # 表格内容插入
        tab_info = str(tab)
        space = 7

        file_path_url = '/home/HelloWorld/'
        # file_path_url = '/Users/chengyan/Desktop/Python/HelloWorld/'

        # PIL模块中，确定写入到图片中的文本字体
        font = ImageFont.truetype('{0}collect_static/uploads/楷体_GB2312.ttf'.format(file_path_url), 30, encoding='utf-8')
        # Image模块创建一个图片对象
        im = Image.new('RGB', (10, 10), (255, 255, 255, 0))
        # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
        draw = ImageDraw.Draw(im, "RGB")
        # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
        img_size = draw.multiline_textsize(tab_info, font=font)
        # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
        im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
        del draw
        del im
        draw = ImageDraw.Draw(im_new, 'RGB')
        # 批量写入到图片中，这里的multiline_text会自动识别换行符
        # python2
        # draw.multiline_text((space, space), unicode(tab_info, 'utf-8'), fill=(255, 255, 255), font=font)
        # python3
        draw.multiline_text((space, space), tab_info, fill=(0, 0, 0), font=font)
        file_path = os.path.join('{0}collect_static/uploads/12345.png'.format(file_path_url))
        im_new.save(file_path)

        del draw
        try:
            res = qiniuuploader.qiniu_upload(file_path)
            result['pic'] = res
        except Exception as e:
            print(e)
        return result

    def dingTalk(self,params):
        title = params['title']
        subtitle = '线上最新版{0}-{1}crash率为{2}'.format(params['appName'], params['version'], params['crash'])
        text =  "### {0}\n".format(title) +\
                        "> {0}\n\n".format(subtitle) +\
                        "> ![screenshot]({0})\n".format(params['pic']) +\
                        "> ###### {0}-{1} [查看详情]({2}) \n".format(params['appName'], params['version'], params['url'])
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": '##{0}'.format(title),
                "text": text
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": False
            }
        }
        json_data = json.dumps(data)
        return json_data

    def test(self):
        b = BuglyData(app_name='haha',app_version='6.3.7')
        b.save()

    def ding(self,params):
        pass


