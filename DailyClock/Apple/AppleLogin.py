#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 11:38 下午
# @Author  : chengyan
# @File    : AppleLogin.py
# @Software: macos
from jwt.algorithms import RSAAlgorithm
import jwt
import simplejson
import requests

TEAM_ID = ''
BUNDLE_ID = 'com.chengyan.DailyClock'

TOKEN_URL = 'https://appleid.apple.com/auth/keys'
def decode_jwt(data):
    # 从苹果那里拿公钥
    key_req = requests.get(TOKEN_URL).json()
    # 从data那里拿到token的加密方式
    head = jwt.get_unverified_header(data)
    token_key = head['kid']
    # 找到相对应的公钥，一般会发布多个公钥
    for pub_key in key_req['keys']:
        if pub_key['kid'] == token_key:
            key_core = simplejson.dumps(pub_key)
            # 打包公钥
            key = RSAAlgorithm.from_jwk(key_core)
            alg = pub_key['alg']
            break
    else:
        print('Unable to find public key')
        return None
    # 使用公钥来解密
    claims = jwt.decode(data, key=key, verify=True, algorithms=[alg], audience=BUNDLE_ID)
    return claims