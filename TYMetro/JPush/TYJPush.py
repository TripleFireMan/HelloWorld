#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 5:40 下午
# @Author  : chengyan
# @File    : TYJPush.py
# @Software: macos

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import base64
import requests
import json

PREFIX = '-----BEGIN RSA PRIVATE KEY-----'
SUFFIX = '-----END RSA PRIVATE KEY-----'

prikey = '''MIICXQIBAAKBgQDB+Q+/Li0t3o4l/Z0MAiO6HenzovcUaQvsdxTz75XfO7wKjGhJ
ChifpTdX5QE2jjCDuygJgjbKMoBdTV/SskkRqUuHZjvvh8U3M/LKGp7dGXNVrfsD
LcWcJDFVKrS0X0D769TAhY+ocXqT4g+jFrnKTVJOUkIM7vJrpDguj8NIJwIDAQAB
AoGBAIQ1exsmoRqbj62rP+iYaLuJehVapSffNYZV4A0n5rIB5/gUnVvzKrddh+w7
pWkG32BaJz7b5vZIF6AAheh5Jj1X+ENn/7fOxoYigrH5YOMTOgG1J1wC65j3nPAV
IAendY9vcjPDNt72G5MT1FG7yI5KD9pdpCAAM+9MiAD2GkRBAkEA7pyRwtFBQsYw
W/Ut6BIHjJY8su4ohWMxHHpWIudTYxi8FGUJjk7g3OtayA/dUaUOiiFVaK7Yobhx
Zk4TSbvIBwJBANAbu4qPexsMfU3fnHAP7eC8rWzc1TBQykAOqPYXupwnwFq8lvkG
qnMU1G73HY05ffAq72D79s+5A8IpjVaBNuECQQCmpWzbnh+xDg+6OasdGHJzSn4M
DW75ccRb+kjsSZkgbab1q3cYD5jWUf1uGj5dBiT4bb1jxjGACPwSEldAOMjDAkBl
7z+UZiVRoXN7Am2ZAmRtMV3tNdoC2X/Hkqa2K/dO57WzfC6i+d3hkrFfTRGfjCqg
yhcItUI2ixRJNZsyZQZhAkA2L0U3RlSfeaEIxVWkh8BPhLr5EQb41ZBL7lCQKIeu
Cf2rwVQM2iPPUtyosE6twjB0zXQ2P3l3OGes28V9xxBs'''

key = "{}\n{}\n{}".format(PREFIX, prikey, SUFFIX)
cipher = PKCS1_v1_5.new(RSA.import_key(key))

def get_phone_number(token):
    url = 'https://api.verification.jpush.cn/v1/web/loginTokenVerify'
    payloadDic = {
        'loginToken':token
    }
    payload = json.dumps(payloadDic)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MDgyZTRjNDUzOTY3MWE2NzdkNGY3YTc0OjkwNDM4MmM2YjQ4OTY1ZDkwMGNlOTMzNQ=='
    }
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.content)
    print(json_data)
    try:
        if  json_data['phone'] is not None:
            phone_encode = json_data['phone']
            phone = cipher.decrypt(base64.b64decode(phone_encode), None).decode()
            return phone
        else:
            return ''
    except Exception as e:
        return ''









