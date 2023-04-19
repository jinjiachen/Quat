#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2022-04-15
'''

import requests
from xq import load_config

def notify(method,title,content):
    '''
    功能：推送消息
    title:消息的标题
    content:消息的内容

    '''
    conf=load_config()#读取配置文件
    token=conf.get('pushplus','token')#获取配置文件中的token

    if method=='get':
        if isinstance(content,str):
            url=f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'#构建get请求的地址
        elif isinstance(content,list):
            pass
    
    
        res=requests.get(url)#发送get请求
        print(res.status_code)
        print(res.url)
    elif method=='post':
        url='http://www.pushplus.plus/send/'
        data={
                'token':f'{token}',
                'title':f'{title}',
                'content':f'{content}'
                }
        res=requests.post(url,data=data)
        print(res.status_code)
        print(data)
