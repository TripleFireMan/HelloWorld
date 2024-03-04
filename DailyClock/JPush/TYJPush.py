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
from logging import getLogger

logger = getLogger('HelloWorld')

PREFIX = '-----BEGIN RSA PRIVATE KEY-----'
SUFFIX = '-----END RSA PRIVATE KEY-----'

prikey = '''MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALDUROK0ve6Fnhup
x2/MFc1VjRwhpOGwYle26zYdgoMvVzAU+nrseQe8ExF/TubqiBrYLjgRPj3YHTzO
LtCs2Uvlpzs7Fn2xS33VPyDv+U2rjg1ShY8mr+QJ3fgcnFMgWnbiPD0JG9g0edzK
wK/7wQZBi4UWRMx1z4x3mc79x6CJAgMBAAECgYBnfDK8Qm6NMuFu6xNumA+CVbj5
Z68o7aMAFmrdBrQktgXee8iDO/Uw056NNOYmOcdhfna+FUlJxDqIJVo8gYvA5vSr
PQFtkvrnYpgftxiGdwb5XsKENnzfQQ3NcAghuiZ6A2MfwASPnNqg/DuvCNX/4uVq
aOT54c2CQeSrpTY3SQJBAOqHAXg47lMgormUZjyzDRr0aIHjXLqBFf2x6xZZMsHk
YaqZRbr7zFi0W3lyS81ZzmK8ltWTFvi5DijL9LHrPFMCQQDBBOX00G8L4QSxz18C
TQKIlLqF0yEMZOlSGiVqL03m0sC3jjoY+rzH7suxvL3ioCKLpY1qJd6c2ZfnCJsu
d3QzAkEAgiUJG738AwVJR9KiKWzzCNI4bFvPSW/41B+3ZV96Wz5xNEp595ljfJYZ
bPuQNRRxAznEOiC1zrBiuyDzWQhBIQJBAJIRHeBtF4v6xe21S2XXV1J6ksiRJJJX
j0XFaYj4sVA7LwH5TLf4j4IRkO45Mc1dd6cMKn8ol1VFSTHaDm1UkocCQQCXcCsf
dn05gD3QXrAz7+QA9dz/sudkBbnxoNSNDXamytBxmSSXhYqhxkNHTLDqp2EI02VV
sWF3a2b70YrQI+zU'''

key = "{}\n{}\n{}".format(PREFIX, prikey, SUFFIX)
cipher = PKCS1_v1_5.new(RSA.importKey(key))

def get_phone_number(token):
    url = 'https://api.verification.jpush.cn/v1/web/loginTokenVerify'
    payloadDic = {
        'loginToken':token
    }
    payload = json.dumps(payloadDic)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZmVlZGEzYzJlMjBiNTllNDMxY2JmZDQzOjJiOTE0NGViOWQ0NDE2YzA5MGY1ZTk3Nw=='
    }
    logger.info(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.content)
    logger.info(json_data)
    try:
        if  json_data['phone'] is not None:
            phone_encode = json_data['phone']
            phone = cipher.decrypt(base64.b64decode(phone_encode), None).decode()
            return phone
        else:
            return ''
    except Exception as e:
        return ''









