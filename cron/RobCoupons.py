#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/10 9:39 上午
# @Author  : chengyan
# @File    : RobCoupons.py
# @Software: macos

import requests
from datetime import datetime
from time import sleep
from threading import Thread
import json
import pickle
def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper

def rob_with_sleep_30s():
    rob_sleep_time(53,1,10,50)

def rob_sleep_time(sleeps,interval,step,robtimes):
    # 沉睡时间
    print('{0}--准备沉睡{1}秒'.format(datetime.now(),sleeps) )
    sleep(sleeps)
    print('复活了，一共要执行{0}次================='.format(step))
    # 复活计数
    lifes = 0
    while lifes < step:
        lifes += 1
        sleep(interval)
        print('沉睡-----------{0}秒'.format(interval))
        rob_times(robtimes)
    print('任务执行结束')

def rob_50_times():
    rob_times(50)

def rob_10_times():
    rob_times(10)

def rob_times(times):
    c = 0
    while c < times:
        c+=1
        rob()

@async_call
def rob():
    rob_wrf()
    # rob_cy()


def rob_wrf():

    url = "https://nb.quanqiuwa.com/api/coupons/app/receive/coupon"

    payload = "{\"storeId\":\"115\",\"couponNo\":\"21DO7\"}"
    headers = {
        'Host': 'nb.quanqiuwa.com',
        'Cookie': 'acw_tc=2760821f16390993884933559e6e22ba828bdc2d9b849561438e7fbad51d24; cna=b032384082ae470eb8bf188e33730108',
        'Accept': '*/*',
        'x-qqw-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUFAiLCJpc3MiOiJTZXJ2aWNlIiwiZXhwIjoxNjQxNjM4OTEwLCJpYXQiOjE2MzkwNDY5MTAsImN1cnJlbnRfdXNlciI6IntcImNoYW5uZWxOb1wiOlwiS0pMSkMySjdJOVwiLFwiY3VzdG9tZXJJZFwiOjMxMjQ2ODcsXCJjdXN0b21lck5vXCI6XCIwMDAxa2NnbVNlNllcIixcImxvZ2luQ2hhbm5lbFwiOlwiQVBQXCIsXCJzZXNzaW9uS2V5XCI6XCI0eFRscFZmc0pmRnlcIixcInVzZXJJZFwiOjMxMjQ2ODd9In0.qYh5lUlD7pSLOVdtL1g2YeCbLMczUCujhxydxZ6B4QU',
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'channelNo': 'KJLJC2J7I9',
        'x-qqw-request-sign': 'mBCEJ6SM9sqgO3rdde+ePYi8ucTWsTLrbnXlhzMXBoA=',
        'x-qqw-channel-no': 'KJLJC2J7I9',
        'clientType': 'iOS,iPhone 14.8.1',
        'x-qqw-client-type': 'iOS,iPhone 14.8.1',
        'User-Agent': 'customer_qqw/3.5.3 (iPhone; iOS 14.8.1; Scale/3.00)',
        'x-qqw-request-nonce': '1639099400',
        'x-qqw-client-version': 'iOS-KJLJC2J7I9-3.5.3',
        'clentVersion': '3.5.3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def rob_cy():
    url = "https://nb.quanqiuwa.com/api/coupons/app/receive/coupon"

    payload = "{\"storeId\":\"6949\",\"couponNo\":\"123\"}"
    payload = json.loads(payload)
    payload["couponNo"] = getCoupon()
    payload = json.dumps(payload).replace(" ","")
    print(payload)
    headers = {
        'Host': 'nb.quanqiuwa.com',
        'Cookie': 'acw_tc=2760821916365378446622661e4e8220dfaf88245a47a8e3887fa3d04272ea',
        'Accept': '*/*',
        'x-qqw-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUFAiLCJpc3MiOiJTZXJ2aWNlIiwiZXhwIjoxNjM5MTMwMDIyLCJpYXQiOjE2MzY1MzgwMjIsImN1cnJlbnRfdXNlciI6IntcImNoYW5uZWxOb1wiOlwiS0pMSkMySjdJOVwiLFwiY3VzdG9tZXJJZFwiOjY3MDYxNyxcImN1c3RvbWVyTm9cIjpcIjAwMDE3NGM5MnIwQVwiLFwibG9naW5DaGFubmVsXCI6XCJBUFBcIixcInNlc3Npb25LZXlcIjpcIlpvSU10dWNuSEs4MFwiLFwidXNlcklkXCI6NjcwNjE3fSJ9.qpYVUh79n-8Hz5YHloAyzqEE2co9dKDUooKdxx4qipQ',
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'channelNo': 'KJLJC2J7I9',
        'x-qqw-request-sign': 'l8J3y8bijqZdayqCUQBIemkErrOHKd0p8Bss9kIbRGg=',
        'x-qqw-channel-no': 'KJLJC2J7I9',
        'clientType': 'iOS,iPhone 14.7',
        'x-qqw-client-type': 'iOS,iPhone 14.7',
        'User-Agent': 'customer_qqw/3.5.3 (iPhone; iOS 14.7; Scale/3.00)',
        'x-qqw-request-nonce': '1636538037',
        'x-qqw-client-version': 'iOS-KJLJC2J7I9-3.5.3',
        'clentVersion': '3.5.3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)




# 定时去替换要抢的券
def requestCurrentCoupon():

    url = "https://nb.quanqiuwa.com/api/merchants/app/pageDecoration/getPageInfo/143941"

    payload = {}
    headers = {
        'Host': 'nb.quanqiuwa.com',
        'Cookie': 'acw_tc=2760822416386076379225692efce8e6e751ec692a1e184e958970a6f4558f; cna=b032384082ae470eb8bf188e33730108',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'x-qqw-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUFAiLCJpc3MiOiJTZXJ2aWNlIiwiZXhwIjoxNjQxMTk2ODY4LCJpYXQiOjE2Mzg2MDQ4NjgsImN1cnJlbnRfdXNlciI6IntcImNoYW5uZWxOb1wiOlwiS0pMSkMySjdJOVwiLFwiY3VzdG9tZXJJZFwiOjMxMjQ2ODcsXCJjdXN0b21lck5vXCI6XCIwMDAxa2NnbVNlNllcIixcImxvZ2luQ2hhbm5lbFwiOlwiQVBQXCIsXCJzZXNzaW9uS2V5XCI6XCI0eFRscFZmc0pmRnlcIixcInVzZXJJZFwiOjMxMjQ2ODd9In0.juSNBpZXKPn_qqvYhZEKIi9QBAmgWunwASh2loQEBHI',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'channelNo': 'KJLJC2J7I9',
        'x-qqw-request-sign': 'YlyZ1B3gGuzCcVqrTbj4ePlDZ8hTCqpyhQXLDfSuhWw=',
        'x-qqw-channel-no': 'KJLJC2J7I9',
        'clientType': 'iOS,iPhone 14.8.1',
        'x-qqw-client-type': 'iOS,iPhone 14.8.1',
        'User-Agent': 'customer_qqw/3.5.3 (iPhone; iOS 14.8.1; Scale/3.00)',
        'x-qqw-request-nonce': '1638607659',
        'x-qqw-client-version': 'iOS-KJLJC2J7I9-3.5.3',
        'clentVersion': '3.5.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    returndata = json.loads(response.text)
    arr = returndata["data"]["pageModuleList"]
    for obj in arr:
        if obj["moduleType"] == 1:
            pmlist = obj["pmContentList"]
            # print(pmlist)
            if len(pmlist) == 1 and pmlist[0]["linkType"] == 16:
                couponNo = pmlist[0]["linkValue"]
                coupon = open('coupon','wb')
                pickle.dump(couponNo,coupon)
                print(pmlist)
                print('获取到最新的券:{0}'.format(couponNo))
# 获取本地存着要抢的券
def getCoupon():
    coupon = open('coupon','rb')
    couponno = pickle.load(coupon)
    return  couponno

if __name__ == '__main__':
    # pass
    # rob_with_sleep_30s()
    # testpicker()
    # readpicker()
    rob_wrf()
    # rob_cy()
    # requestCurrentCoupon()
    # coupon = '123'
    # storeId = 'storeid'
    # payload = f"""{{"storeId":"6949","couponNo":{coupon}}}"""
    # print(payload)