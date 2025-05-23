"""
Django settings for HelloWorld project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
import django
from HelloWorld.config import MyConfig
import SportRecord
# from rest_framework import routers, serializers, viewsets

my_config = MyConfig()
my_config.setup_logging()
conf = my_config.get_conf()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!lq6&3dj1f9ttdz34ugknhf)ac-4!s5is)tj=)j!4t5urj#@y^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = conf.DEBUG
TEMPLATE_DEBUG = conf.DEBUG
ALLOWED_HOSTS = ['*']

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    # 'simpleui',
    'grappelli',
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 验证电话号码
    "phonenumber_field",
    # 图片上传模块 django-filer
    'easy_thumbnails',
    'filer',
    'mptt',
    'rest_framework',
    'rest_framework_jwt',
    'TestModel',
    'DailyClock',
    'django_apscheduler',  # 定时执行任务
    'TYMetro',
    'ZhuaZhou',
    'SportRecord',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'SportRecord.middleware.JwtAuthenticationMiddleware',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
PHONENUMBER_DEFAULT_REGION = 'CN'# 例如，设置为中国
# 配置跨域访问
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['*','PUT']
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated'
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_PAGINATION_CLASS': 'SportRecord.pagination.SportRecordNumberPagination',
    'DEFAULT_FILTER_BACKENDS' :['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 10,  # 每页显示的条目数
    'SEARCH_PARAM' : 'query'
}

JWT_AUTH = {
    # 设置token有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1)
}

ROOT_URLCONF = 'HelloWorld.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis服务器地址和数据库编号
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


WSGI_APPLICATION = 'HelloWorld.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = conf.DATABASES

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    "TYMetro.views.CustomAuth"
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "TYMetro.UserProfile"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 支持视网膜高分辨率设备
THUMBNAIL_HIGH_RESOLUTION = False
THUMBNAIL_ALIASES = {
'': {
    'small': {'size': (180, 180), 'crop': True},
    'big':{'size':(360,360),'crop':True},
},
}
# 处理缩列图
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# 存放图片文件夹设置
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': '/mnt/sdc/HelloWorld/media/filer',
                'base_url': '/media/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': '/mnt/sdc/HelloWorld/media/filer_thumbnails',
                'base_url': '/media/filer_thumbnails/',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': '/mnt/sdc/HelloWorld/media/smedia/filer',
                'base_url': '/smedia/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': '/mnt/sdc/HelloWorld/media/smedia/filer_thumbnails',
                'base_url': '/smedia/filer_thumbnails/',
            },
        },
    },
}

  
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_ROOT = '/mnt/sdc/HelloWorld/media'
MEDIA_URL = '/media/'


STATICFILES_DIRS = (
    os.path.join(os.path.join(MEDIA_ROOT)),
    os.path.join(BASE_DIR, 'templates/resources'),
    os.path.join(BASE_DIR, 'DailyClock', 'static'),
    os.path.join(django.__file__.rstrip('__init__.py'), 'contrib/admin/static/admin').replace('\\', '/'),
    # os.path.join(BASE_DIR, 'templates'),
    # os.path.join(BASE_DIR, 'templates'),
)

# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# 设置每分钟执行一个任务，并将日志输出到指定文件
# python manage.py crontab add　　添加定时任务
# python manage.py crontab remove 清除定时任务
# python manage.py crontab show   显示定时任务
CRONJOBS = [
    # ('*/1 * * * *','HelloWorld.view.print_110','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('58 15 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('59 15 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('00 16 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('58 17 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('59 17 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('00 18 10 * *','cron.RobCoupons.rob_50_time','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log')),
# ('31 * * * *','cron.RobCoupons.rob_with_sleep_30s','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'test.log')),
# ('* * 18 7 *','cron.RobCoupons.rob_with_sleep_30s','>> ' + os.path.join(os.path.dirname(BASE_DIR), 'test.log')),
]
#
# # 定时任务设置中文字符，如py果不设置的话，可能会出现字符异常
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_CN.UTF-8'

