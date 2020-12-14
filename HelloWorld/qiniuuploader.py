#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/13 9:38 下午
# @Author  : chengyan
# @File    : qiniu.py
# @Software: macos

import qiniu
import logging

access_key = 'v_Uty5Twt_JofcObigIeM-CUZYKA00Sd2MzsJ3K4'
secret_key = 'qWhhplSFLDKhZ42Sk_h31l1xl636zFcGy273VJSv'
url = 'http://yun.chengyan.shop/'
bucket_name = 'quanqiuwa251'
logger = logging.getLogger('HelloWorld.qiniu')

def qiniu_upload(localfile):
    file_key = qiniu.etag(localfile) + '.png'
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, file_key, 3600)
    ret, info = qiniu.put_file(token, file_key, localfile)
    if ret:
        logger.info(ret)
        return '{0}{1}'.format(url, ret['key'])
    else:
        logger.error(ret)
        raise print('上传失败，请重试')


if __name__ == '__main__':
    localfile = '/Users/chengyan/Desktop/WechatIMG1782.jpeg'
    res = qiniu_upload(localfile)
    print(res)

