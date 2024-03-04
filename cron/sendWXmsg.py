#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/7 5:29 下午
# @Author  : chengyan
# @File    : sendWXmsg.py
# @Software: macos
import requests
import json
import itchat
from itchat.content import *

# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
    appkey = "3d7807ed50164292b746d98cac705ed3"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    itchat.send('%s' % tuling(msg['Text']),msg['FromUserName'])


if __name__ == '__main__':
    # itchat.auto_login(hotReload=True)
    itchat.login()
    userfinfo = itchat.search_friends("王瑞芳")
    print(userfinfo)
    itchat.run()

