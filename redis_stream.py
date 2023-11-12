#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-11-10
'''

import json,os
from walrus import Database
from configparser import ConfigParser
from trade_xq import *


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
d=u2_connect(conf)
token=conf.get('redis','token')
db = Database(
    host='redis-16873.c294.ap-northeast-1-2.ec2.cloud.redislabs.com',
    port=16873,
    password=token, 
    decode_responses=True)


def order_handle(msg):
    # 请在此处自己coding, 根据msg给交易端下单
#    print(msg)
    for single in msg:
        print(f'正在处理{single}')
        data=single[1]
        act=data['action']
        code=data['code']
        code=transfer_code(code)#转换成雪球股票代码
        pct=data['pct']
        if act=='BUY':
            print(f'BUY {code}')
            ready(d,conf)
            buy(d,code,'100','')
        elif act=='SELL':
            print(f'SELL {code}')
            ready(d,conf)
            sell(d,code,'100','')

###转换不同平台的股票代码
def transfer_code(code):
    if 'XSHE' in code:
        data=code.split('.')
        new_code='SZ'+data[0]
    elif 'XSHG' in code:
        data=code.split('.')
        new_code='SH'+data[0]
    return new_code

###启动stream模式
stream = db.Stream('xq')
while True:
    item = stream.read(count=100, block=1000, last_id='$')
    if item:
#        order_handle(item)
        print(item)
