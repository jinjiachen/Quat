#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-11-10
'''

import json,os
from walrus import Database
from configparser import ConfigParser


def load_config():#加载配置文件
    conf=ConfigParser()
    if os.name=='nt':
#        path='K:/config.ini'
        path=r'D:\Downloads\PortableGit-2.36.1-64-bit.7z\bin\Quat\config.ini'
    elif os.name=='posix':
        path='/usr/local/src/Quat/config.ini'
    else:
        print('no config file was found!')

    conf.read(path,encoding="utf-8")
    return conf


conf=load_config()
token=conf.get('redis','token')
db = Database(
    host='redis-16873.c294.ap-northeast-1-2.ec2.cloud.redislabs.com',
    port=16873,
    password=token, 
    decode_responses=True)


stream = db.Stream('xq')
while True:
    item = stream.read(count=1, block=1000, last_id='$')
    if item:
        print(item)


def order_handle(msg):
    # 请在此处自己coding, 根据msg给交易端下单
    print(msg)


