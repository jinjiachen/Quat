#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-09-25
'''
import uiautomator2 as u2
import time
import os

###连接手机
def u2_connect():
    d=u2.connect('192.168.2.107:37423')
    print(d.info)
    return d


###停留在指定的界面
def ready(d):
    app=d.app_current()['package']
    if app=='com.hwabao.hbstockwarning':#当前app是否为证券app
        while True:
            if d(resourceId="com.hwabao.hbstockwarning:id/tab_text", text="我的").exists:
                d(text="资金持仓").click()
                break
            else:
                print('不在初始界面，正在返回')
                d.press('back')
    else:
        d.app_start('com.hwabao.hbstockwarning')#打开证券app
        d(text="资金持仓").click()

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
    count=d(resourceId="com.hwabao.hbstockwarning:id/txt_name").count
    res=[]
    for i in range(0,count):
        name=d(resourceId="com.hwabao.hbstockwarning:id/txt_name")[i].get_text()
        res.append(name)
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
    os.system('adb shell input text {}'.format(number))

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
    os.system('adb shell input text {}'.format(number))
    d(description="卖出").click()
    d(description="确认卖出").click()
    print(f'正在卖出{stock_code},数量:{number}')


###主程序
if __name__=='__main__':
    d=u2_connect()
    ready(d)
    time.sleep(0.5)
    res=account(d)
    print(res)
    stocks=position(d)
    print(stocks)
    start=time.time()
#    buy(d,'600592','200')
    sell(d,'000592','200')
    end=time.time()
    print('用时：',end-start)
