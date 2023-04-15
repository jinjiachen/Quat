#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2022-04-15
'''

import requests
from xq import load_config

def notify(title,content):
    '''
    功能：推送消息
    title:消息的标题
    content:消息的内容
    '''
    conf=load_config()#读取配置文件
    token=conf.get('pushplus','token')#获取配置文件中的token
#    content='this is a test'
#    title='debug'
    url=f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'#构建get请求的地址
    res=requests.get(url)#发送get请求
    print(res.status_code)
    print(res.url)
