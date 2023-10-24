#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-10-24
'''
import json
import redis
from configparser import ConfigParser
import os


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

def order(sig):
    mycmd = '{} {} zxjg {} -notip'.format(sig['action'], sig['zqdm'], sig['qty'])
    print(mycmd)


def main(conf):
    token=conf.get('redis','token')
    r = redis.Redis(
        host='redis-16873.c294.ap-northeast-1-2.ec2.cloud.redislabs.com',
        port=16873,
        password=token)
    ps = r.pubsub()
    ps.subscribe('myChannel')
    for item in ps.listen():  # keep listening, and print the message in the channel
        if item['type'] == 'message':
            signals = item['data'].decode('utf-8')
            if signals == 'exit':
                break
            else:
                signal_list = json.loads(signals)
                for sig in signal_list:
                    print(sig)
#                    order(sig)


if __name__ == '__main__':
    conf=load_config()
    main(conf)
