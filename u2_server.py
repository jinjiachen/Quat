
#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-12-13
'''
import uiautomator2 as u2
import time
import os
from configparser import ConfigParser


###读取配置文件
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


###连接手机
def u2_connect(conf):
    try:
        print('正在尝试有线连接!')
        d=u2.connect()
        print(d.info)
    except:
        print('正在尝试无线连接!')
        addr=conf.get('adb','ip')
        cmd=f'adb connect {addr}'
        print(cmd)
        if os.name=='posix':
            os.system(cmd)
        elif os.name=='nt':
            os.system(f'D:\Downloads\scrcpy-win64-v2.1\\{cmd}')
        d=u2.connect(addr)
        print(d.info)
    return d


###检查ui2服务是否运行
def check_status(d):
    now=time.strftime("%H:%M:%S")
    if d.service('uiautomator').running():
        print(f'{now}servise running')
    else:
        print('starting servise')
        d.service(f'{now} uiautomator').start()

if __name__=='__main__':
    conf=load_config()
    d=u2_connect(conf)
    while True:
        check_status(d)
