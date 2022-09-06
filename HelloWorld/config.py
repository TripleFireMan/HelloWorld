#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/14 9:49 上午
# @Author  : chengyan
# @File    : config.py
# @Software: macos
import os
import logging
import logging.config
import json
import sys

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
logger = logging.getLogger('HelloWorld')

class local():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hello',
            'USER': 'root',  # 你的用户名
            'PASSWORD': '88888888',  # 你的密码
            'HOST': '0.0.0.0',  # 你的IP地址
            'PORT': '3306',  # 你的端口号
            'OPTIONS': {'charset': 'utf8mb4',
                        "init_command":"SET foreign_key_checks = 0;",
                        },
        }
    }
    DEBUG = True

class remote():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hello',
            'USER': 'root',  # 你的用户名
            'HOST': '39.96.77.250',  # 你的密码
            'PASSWORD': 'Chengyan#251',  # 你的IP地址
            # 'PASSWORD': '88888888',  # 你的密码
            # 'HOST': '0.0.0.0',  # 你的IP地址
            'PORT': '3306',  # 你的端口号
            'OPTIONS': {'charset': 'utf8mb4',
                        "init_command":"SET foreign_key_checks = 0;",
                        },
    }
    }
    DEBUG = False

class MyConfig():
    __conf = None
    __is_remote = not RUNNING_DEVSERVER

    def is_remote_env(self):
        return self.__is_remote

    def get_conf(self):
        if  self.__conf == None:
            if self.__is_remote:
                logger.info('当前数据库运行在正式环境')

                self.__conf = remote()
            else:
                logger.info('当前数据库运行在测试环境')
                self.__conf = local()
        return self.__conf

    def setup_logging(self,default_path="loggerConfig.json", default_level=logging.INFO, env_key="LOG_CFG"):
        path = os.path.join(os.path.abspath('HelloWorld'),default_path)
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, "r") as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
