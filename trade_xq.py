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
#        ready(d,conf)
        res=position(d)
        print(res)
    elif choice=='act':
        ready(d,conf)
        res=account(d)
        print(res)
    elif choice=='buy':
        stock_code=input('请输入股票代码:')
        price=input('请输入买入价格：')
        number=input('请输入买入数量：')
        buy(d,stock_code,price,number)
    elif choice=='sell':
        stock_code=input('请输入股票代码:')
        price=input('请输入卖出价格：')
        number=input('请输入卖出数量：')
        sell(d,stock_code,price,number)

###停留在指定的界面
def ready(d,conf):
    '''
    d(obj):u2对象
    conf:load_conf返回结果
    '''
    app=d.app_current()['package']
#    print(app)
    if app=='com.xueqiu.android':#当前app是否为证券app
        while True:
#            if d(resourceId="com.xueqiu.android:id/broker_name").exists:
            if d(text="沪深").exists:
                print('在指定界面')
                break
            else:
                print('不在初始界面，正在返回')
                d.press('back')
                if d(resourceId="com.xueqiu.android:id/tab_name", text="我的").exists:
                    d(resourceId="com.xueqiu.android:id/tab_name", text="我的").click()
                    d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").click()
                    break
    else:
        print('正在打开应用！')
        d.app_start('com.xueqiu.android')#打开证券app
        d(resourceId="com.xueqiu.android:id/tab_name", text="我的").click()
        d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").click()
        while True:
            if d(text="请输入交易密码").exists:
                print('正在输入密码')
                token=conf.get('adb','token')
                passwd=base64.b64decode(token).decode('ascii')
    #            print(passwd)
                if os.name=='posix':
                    os.system('adb shell input text {}'.format(passwd))
                elif os.name=='nt':
                    os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(passwd))
                break
            elif d(text="沪深").exists:
                print('在指定界面')
                break

###查询帐户基本信息
def account(d):
    '''
    d(obj):u2连接对象
    函数返回float类型
    '''
    res={}
    assets=d(resourceId="com.xueqiu.android:id/asset_balance").get_text()#总资产
    value=d(resourceId="com.xueqiu.android:id/value")[0].get_text()#持有市值
    profit=d(resourceId="com.xueqiu.android:id/value")[1].get_text()#盈亏
    available=d(resourceId="com.xueqiu.android:id/value")[2].get_text()#可用
    res={'assets':assets,
            'value':value,
            'profit':profit,
            'available':available}
    return res


###查询股票持仓
def position(d):
    d(resourceId="com.xueqiu.android:id/column_1_row_1").get_text()#持仓
    return res


###买入操作
def buy(d,stock_code,price,number):
    '''
    d(obj):u2连接对象
    stock_code(str):买入的股票代码，数字部分即可
    price(str):买入的价格
    number(str):买入的数量
    '''
    d(resourceId="com.xueqiu.android:id/trade_action_button_item_title", text="买入").click()
    d(resourceId="com.xueqiu.android:id/order_search_input").click()
    #方法三,速度相对较快
    if os.name=='posix':
        os.system('adb shell input text {}'.format(stock_code))#股票名称
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(stock_code))#股票名称
    d.click(1400,2900)#模拟点击，其他方法无法定位
    d(resourceId="com.xueqiu.android:id/order_input_editText")[0].set_text(price)#价格
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].clear_text()
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].set_text(number)#数量
    d(resourceId="com.xueqiu.android:id/order_submit").click()#提交
#    d(resourceId="com.xueqiu.android:id/tv_right").click()#确定
    print(f'正在买入{stock_code},价格：{price}数量:{number}')


###卖出操作
def sell(d,stock_code,price,number):
    '''
    d(obj):u2连接对象
    price(str):买入的价格
    stock_code(str):买入的股票代码，数字部分即可
    number(str):买入的数量
    '''
    d(resourceId="com.xueqiu.android:id/trade_action_button_item_title", text="卖出").click()
    d(resourceId="com.xueqiu.android:id/order_search_input").click()
    #方法三,速度相对较快
    if os.name=='posix':
        os.system('adb shell input text {}'.format(stock_code))
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(stock_code))
    d.click(1400,2900)#模拟点击，其他方法无法定位
    d(resourceId="com.xueqiu.android:id/order_input_editText")[0].set_text(price)#价格
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].clear_text()
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].set_text(number)
    d(resourceId="com.xueqiu.android:id/order_submit").click()
#    d(resourceId="com.xueqiu.android:id/tv_right").click()#确定
    print(f'正在卖出{stock_code},价格:{price}数量:{number}')


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
