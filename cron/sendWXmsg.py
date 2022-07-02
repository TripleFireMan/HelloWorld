#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/7 5:29 下午
# @Author  : chengyan
# @File    : sendWXmsg.py
# @Software: macos
import itchat



if __name__ == '__main__':

    itchat.auto_login(hotReload=True)
    userfinfo = itchat.search_friends("王瑞芳")
    print(123)
