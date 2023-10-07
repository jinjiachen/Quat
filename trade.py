#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-09-25
'''
import uiautomator2 as u2
import time
import os
import base64
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



###菜单
def menu():
    choice=input('pos:查询股票持仓\nact:查询资金情况\nbuy:买入股票\nsell:卖出股票')
#    d=u2_connect()
    if choice=='pos':
        ready(d,conf)
        res=position(d)
        print(res)
    elif choice=='act':
        ready(d,conf)
        res=account(d)
        print(res)
    elif choice=='buy':
        stock_code=input('请输入股票代码:')
        number=input('请输入买入数量：')
        buy(d,stock_code,number)
    elif choice=='sell':
        stock_code=input('请输入股票代码:')
        number=input('请输入卖出数量：')
        sell(d,stock_code,number)

###停留在指定的界面
def ready(d,conf):
    '''
    d(obj):u2对象
    conf:load_conf返回结果
    '''
    app=d.app_current()['package']
    if app=='com.hwabao.hbstockwarning':#当前app是否为证券app
        while True:
            if d(resourceId="com.hwabao.hbstockwarning:id/tab_text", text="我的").exists:
                d(text="资金持仓").click()
                time.sleep(0.5)
                break
            else:
                print('不在初始界面，正在返回')
                d.press('back')
    else:
        d.app_start('com.hwabao.hbstockwarning')#打开证券app
        d(text="交易").click()
        d(text="资金持仓").click()
        while True:
            if d(text="请输入交易密码").exists:
                token=conf.get('adb','token')
                passwd=base64.b64decode(token).decode('ascii')
    #            print(passwd)
                if os.name=='posix':
                    os.system('adb shell input text {}'.format(passwd))
                elif os.name=='nt':
                    os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(passwd))
                break

###查询帐户基本信息
def account(d):
    '''
    d(obj):u2连接对象
    函数返回float类型
    '''
    counts=d(resourceId="com.hwabao.hbstockwarning:id/tv_asset").count
    res={}
    for i in range(0,counts):
        title=d(resourceId="com.hwabao.hbstockwarning:id/tv_title")[i].get_text()
        asset=d(resourceId="com.hwabao.hbstockwarning:id/tv_asset")[i].get_text()
        res[title]=asset
    return res


###查询股票持仓
def position(d):
#    d(text="资金持仓").click()
    time.sleep(1)
    count=d(resourceId="com.hwabao.hbstockwarning:id/txt_name").count
    res={}
    for i in range(0,count):
        content={}
        name=d(resourceId="com.hwabao.hbstockwarning:id/txt_name")[i].get_text()#股票名称
        cost=d(resourceId="com.hwabao.hbstockwarning:id/txt_cost_price")[i].get_text()#成本价
        current=d(resourceId="com.hwabao.hbstockwarning:id/txt_current_price")[i].get_text()#当前价
        hold=d(resourceId="com.hwabao.hbstockwarning:id/txt_hold_account")[i].get_text()#持仓数量
        available=d(resourceId="com.hwabao.hbstockwarning:id/txt_available_account")[i].get_text()#可用数量
        print(f'{i}/{count}')
        content['cost']=cost
        content['current']=current
        content['hold']=hold
        content['available']=available
        res[name]=content
#        d(resourceId="com.hwabao.hbstockwarning:id/ll_cost")#价格
    return res


###买入操作
def buy(d,stock_code,number):
    '''
    d(obj):u2连接对象
    stock_code(str):买入的股票代码，数字部分即可
    number(str):买入的数量
    '''
    d(text="买入").click()
#    code=d.xpath('//*[@resource-id="com.hwabao.hbstockwarning:id/hqmainview"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]')#点击股票代码输入框
#    code.click()#xpath方法的运行速度还是偏慢
    d(description="输入股票").click()
    d(text=" 请输入股票代码/首字母").click()
    d(text=" 请输入股票代码/首字母").send_keys(stock_code)
#    d(text=" 请输入股票代码/首字母").set_text(stock_code)
    d(text="进入").click()
    amount=d.xpath('//*[@resource-id="com.hwabao.hbstockwarning:id/hqmainview"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]')
    time.sleep(0.5)
    amount.click()
    #方法一,速度慢
#    amount.set_text('100')
    #方法二,速度适中
#    d.set_fastinput_ime(True)
#    d.send_keys('100')
#    d.set_fastinput_ime(False)
    #方法三,速度相对较快
    if os.name=='posix':
        os.system('adb shell input text {}'.format(number))
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(number))

    d(description="买入").click()
    d(description="确认买入").click()
    print(f'正在买入{stock_code},数量:{number}')


###卖出操作
def sell(d,stock_code,number):
    '''
    d(obj):u2连接对象
    stock_code(str):买入的股票代码，数字部分即可
    number(str):买入的数量
    '''
    d(text="卖出").click()
    d(description="输入股票").click()
    time.sleep(0.5)
    d(text="请输入股票代码/首字母").click()
    d(text="请输入股票代码/首字母").send_keys(stock_code)
    d(text="进入").click()
    d.xpath('//*[@resource-id="com.hwabao.hbstockwarning:id/hqmainview"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]').click()
    if os.name=='posix':
        os.system('adb shell input text {}'.format(number))
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(number))
    d(description="卖出").click()
    d(description="确认卖出").click()
    print(f'正在卖出{stock_code},数量:{number}')


###主程序
if __name__=='__main__':
    conf=load_config()
    d=u2_connect(conf)
    while True:
        menu()
#    ready(d)
#    time.sleep(0.5)
#    res=account(d)
#    print(res)
#    stocks=position(d)
#    print(stocks)
#    start=time.time()
#    buy(d,'600592','200')
#    sell(d,'000592','200')
#    end=time.time()
#    print('用时：',end-start)
