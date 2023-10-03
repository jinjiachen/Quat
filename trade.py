#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-09-25
'''
import uiautomator2 as u2
import time
import os


def u2_connect():
    d=u2.connect('192.168.2.107:41023')
    print(d.info)
    return d


###查询帐户基本信息
def account(device):
    '''
    device(obj):u2连接对象
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
def position(device):
    count=d(resourceId="com.hwabao.hbstockwarning:id/txt_name").count
    res=[]
    for i in range(0,count):
        name=d(resourceId="com.hwabao.hbstockwarning:id/txt_name")[i].get_text()
        res.append(name)
    return res


###买入操作
def buy(device):
    d(text="买入").click()
    code=d.xpath('//*[@resource-id="com.hwabao.hbstockwarning:id/hqmainview"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]')#点击股票代码输入框
    code.click()
    d(text=" 请输入股票代码/首字母").click()
    d(text=" 请输入股票代码/首字母").send_keys('600592')
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
    os.system('adb shell input text {}'.format('100'))

    d(description="买入").click()
    d(description="确认买入").click()



###主程序
if __name__=='__main__':
    d=u2_connect()
    res=account(d)
    print(res)
    stocks=position(d)
    print(stocks)
    start=time.time()
    buy(d)
    end=time.time()
    print('用时：',end-start)
