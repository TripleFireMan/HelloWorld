#!/usr/local/bin/python3
# -*- coding:UTF-8 -*-
import requests
import json
import pymysql
import datetime
import time
url0 = 'http://leancloud.emotionwp.com/1.1/classes/dataone2?limit=1&order=-postId&where=%7B%22postId%22%3A%7B%22%24lte%22%3A{0}%7D%7D'

payload={}
headers = {
  'method': 'GET',
  'accept': 'application/json',
  'content-type': 'application/json; charset=utf-8',
  'x-lc-id': 'xrxv6172xjl80hxd7dbvmcuugaq7lo4lla3qqm2h20ld6oo7',
  'x-lc-prod': '1',
  'x-lc-sign': 'c79b53135b6fa1404056a9a18648e026,1606981542123',
  'accept-language': 'zh-Hans-CN;q=1',
  'user-agent': 'LeanCloud-Objc-SDK/12.1.3',
  'accept-encoding': 'gzip'
}
#######################################头部#######################################

# 建表
def create_table(connect):
    create_table = '''
                   create table jitang
                   (id int auto_increment primary key not null,
                   text varchar(255),
                   url varchar(255),
                   wordsInfo varchar(255),
                   width int,
                   height int,
                   date datetime,
                   objectId varchar(255) default NULL COMMENT '唯一ID',
                   unique (objectId))
                   '''
    try:
        result = connect.cursor().execute(create_table)
    except Exception as e:
        print(str(e))
# 抓包
def spider(connect):
    base_date_str = '2021-12-07'
    base_post_id = 1700000308
    base_date = datetime.datetime.strptime(base_date_str,'%Y-%m-%d')
    today = datetime.datetime.now()
    today_post_id = base_post_id +  (today-base_date).days
    url = url0.format(today_post_id)
    response = requests.request("GET", url, headers=headers, data=payload)
    save(response, connect)

def save(response,connect):
    # insert_sql = "replace into jitang(url,text,date,width,height,wordsInfo,objectId) values(%s,%s,%s,%s,%s,%s,%s)"
    # fetch_sql = 'select * from jitang where objectId = {0}'
    insert_sql = '''
                    insert into jitang(url,text,date,width,height,wordsInfo,objectId) 
                    values(%s,%s,%s,%s,%s,%s,%s) 
                    on duplicate key update date='{0}'
                '''.format(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    for obj in response.json()['results']:
        url = "http://emotion.emotionwp.com/" + obj['url'] + '.jpg'
        text = obj['text']
        width = (obj['width'])
        height = (obj['height'])
        words_info = obj['wordsInfo']
        obj_id = str(obj['objectId'])
        date = datetime.datetime.now()
        datestring = date.strftime('%Y-%m-%d %H-%M-%S')
        try:
            with connect.cursor() as cursor:
                cursor.execute(insert_sql, (url, text, datestring, width, height, words_info, obj_id))
                connect.commit()
        except Exception as e:
            print(e)

def do_work():
    connect = pymysql.connect(host='39.96.77.250', user='root', password='Chengyan#251', port=3306, db='hello')
    # 建表
    create_table(connect)
    # 爬
    spider(connect)
    # 关闭
    connect.close()


if __name__ == '__main__':
    do_work()
