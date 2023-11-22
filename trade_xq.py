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
conf=load_config()


###全局变量
device=conf.get('trade','device')
runlevel=conf.get('trade','mode')


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



###菜单
def menu():
    print(f'设备：{device}\n运行模式：{runlevel}')
    choice=input('pos:查询股票持仓\nact:查询资金情况\nbuy:买入股票\nsell:卖出股票\nrepo:逆回购\nbuys:买入一组股票\nsells:卖出一组股票')
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
        ready(d,conf)
        stock_code=input('请输入股票代码:')
        price=input('请输入买入价格：')
        number=input('请输入买入数量：')
        buy(d,stock_code,number,price,mode=int(runlevel))
    elif choice=='sell':
        ready(d,conf)
        stock_code=input('请输入股票代码:')
        price=input('请输入卖出价格：')
        number=input('请输入卖出数量：')
#        sell(d,stock_code,number,price,1)
        sell(d,stock_code,number,price,mode=int(runlevel))
    elif choice=='repo':
        ready(d,conf)
        reverse_repo(d,mode=1)
    elif choice=='buys':
        ready(d,conf)
        data=[('SZ000592','200'),('SH600592','100')]
        buy_group(d,data)
    elif choice=='sells':
        ready(d,conf)
        data=[('SZ000592','200'),('SH600592','100')]
        sell_group(d,data)

###死循环解锁屏幕，确保解锁成功
def wakeup(d,conf):
    '''
    d(obj):u2对象
    conf:load_conf返回结果
    '''
    #检查屏幕状态，如果息屏，点亮并解锁
    if d.info.get('screenOn')==False:#熄屏状态
        d.unlock()
        d.unlock()
        unlock=conf.get('adb','unlock')#解锁密码
        if os.name=='posix':
            os.system('adb shell input text {}'.format(unlock))
        elif os.name=='nt':
            os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(unlock))


###停留在指定的界面
def ready(d,conf):
    '''
    d(obj):u2对象
    conf:load_conf返回结果
    '''

    wakeup(d,conf)#解锁屏幕
    app=d.app_current()['package']
#    print(app)
    if app=='com.xueqiu.android':#当前app是否为证券app
        while True:
#            if d(resourceId="com.xueqiu.android:id/broker_name").exists:
            if d(text="沪深").exists:
                time.sleep(0.5)#防止检测不到解锁
                if d(text='解锁').exists:
                    d(text='解锁').click()
#                    time.sleep(1)
                    check_passwd(d)
                print('在指定界面')
                break
            else:
                print('不在初始界面，正在返回')
                d.press('back')
                if d(resourceId="com.xueqiu.android:id/tab_name", text="我的").exists:
                    d(resourceId="com.xueqiu.android:id/tab_name", text="我的").click()
                    d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").click()
#                    time.sleep(1)
                    check_passwd(d)
                    break
    else:
        if check_running(d,'com.xueqiu.android'):
            print('程序在后台，正在切换应用！')
            d.app_start('com.xueqiu.android')#打开证券app
            time.sleep(1)#等待切换
            if d(text="沪深").exists:
                if d(text='解锁').exists:
                    d(text='解锁').click()
#                    time.sleep(1)
                    check_passwd(d)
                print('已经在指定界面')
            else:
                print('不在初始界面，正在返回')
                while True:
                    d.press('back')
                    if d(resourceId="com.xueqiu.android:id/tab_name", text="我的").exists:
                        d(resourceId="com.xueqiu.android:id/tab_name", text="我的").click()
                    if d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").exists():
                        d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").click()
#                        time.sleep(1)
                        check_passwd(d)
                        break
        else:
            print('正在打开应用！')
            d.app_start('com.xueqiu.android')#打开证券app
            d(resourceId="com.xueqiu.android:id/tab_name", text="我的").click()
            d(resourceId="com.xueqiu.android:id/assets_title", text="股票资产(元)").click()
#            time.sleep(1)
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
    positions=d(resourceId="com.xueqiu.android:id/column_1_row_1")#持仓
    res=[]
    for pos in positions:
        res.append(pos.get_text())
    return res


###买入操作
def buy(d,stock_code,number,price='',mode=0):
    '''
    d(obj):u2连接对象
    stock_code(str):买入的股票代码，数字部分即可
    price(str):买入的价格
    number(str):买入的数量
    mode(int):0-测试模式，1-实战模式
    '''
    d(resourceId="com.xueqiu.android:id/trade_action_button_item_title", text="买入").click()
    time.sleep(0.5)
    check_passwd(d)
    d(resourceId="com.xueqiu.android:id/order_search_input").click()
    #方法三,速度相对较快
    if os.name=='posix':
        os.system('adb shell input text {}'.format(stock_code))#股票名称
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(stock_code))#股票名称
    time.sleep(0.5)#后面是位置点击，这里作必要的停顿
    if device=='mi11':
        d.click(1400,2900)#模拟点击，其他方法无法定位,mi11
    elif device=='redmi':
        d.click(984,1818)#模拟点击，其他方法无法定位,redmi
    if price!='':
        d(resourceId="com.xueqiu.android:id/order_input_editText")[0].set_text(price)#价格
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].clear_text()
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].set_text(number)#数量
    d(resourceId="com.xueqiu.android:id/order_submit").click()#提交
    if mode==1:
        d(resourceId="com.xueqiu.android:id/tv_right").click()#确定
        print(f'正在买入{stock_code},价格：{price}数量:{number}')
    elif mode==0:
        d(resourceId="com.xueqiu.android:id/tv_left").click()#取消
        print(f'测试模式：正在买入{stock_code},价格：{price}数量:{number}')


###买入一组股票
def buy_group(d,data):
    '''
    d(obj):u2连接对象
    data(list):一组股票信息的列表，包含股票代码和数量信息，如：[(stock code, number)]
    '''
    for stock_info in data:
        print(stock_info)
        buy(d,stock_info[0],stock_info[1],'')
        ready(d,conf)#临时办法，待优化


###卖出操作
def sell(d,stock_code,number,price='',mode=0):
    '''
    d(obj):u2连接对象
    price(str):买入的价格
    stock_code(str):买入的股票代码，数字部分即可
    number(str):买入的数量
    mode(int):0-测试模式，1-实战模式
    '''
    d(resourceId="com.xueqiu.android:id/trade_action_button_item_title", text="卖出").click()
    time.sleep(0.5)
    check_passwd(d)
    d(resourceId="com.xueqiu.android:id/order_search_input").click()
    #方法三,速度相对较快
    if os.name=='posix':
        os.system('adb shell input text {}'.format(stock_code))
#        input_text(stock_code)
    elif os.name=='nt':
        os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(stock_code))#股票名称
#        input_text(stock_code)
    time.sleep(0.5)#后面是位置点击，这里作必要的停顿
    if device=='mi11':
        d.click(1400,2900)#模拟点击，其他方法无法定位,mi11
    elif device=='redmi':
        d.click(984,1818)#模拟点击，其他方法无法定位,redmi
    if price!='':
        d(resourceId="com.xueqiu.android:id/order_input_editText")[0].set_text(price)#价格
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].clear_text()
    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].set_text(number)
    d(resourceId="com.xueqiu.android:id/order_submit").click()
    if mode==1:
        d(resourceId="com.xueqiu.android:id/tv_right").click()#确定
        print(f'正在卖出{stock_code},价格:{price}数量:{number}')
    elif mode==0:
        d(resourceId="com.xueqiu.android:id/tv_left").click()#取消
        print(f'测试模式：正在卖出{stock_code},价格:{price}数量:{number}')


###卖出一组股票
def sell_group(d,data):
    '''
    d(obj):u2连接对象
    data(list):一组股票信息的列表，包含股票代码和数量信息，如：[(stock code, number)]
    '''
    for stock_info in data:
        print(stock_info)
        sell(d,stock_info[0],stock_info[1],'')
        ready(d,conf)#临时办法，待优化

###检查是否输入密码
def check_passwd(d,times=10):
    '''
    d(obj):u2连接对象
    times(str):检测次数
    '''
    i=1
    while i<=int(times):
        if d(text="请输入交易密码").exists:
            print('检测到密码，正在输入密码')
            token=conf.get('adb','token')
            passwd=base64.b64decode(token).decode('ascii')
    #        print(passwd)
            if os.name=='posix':
                os.system('adb shell input text {}'.format(passwd))
            elif os.name=='nt':
                os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(passwd))
            break
        i=i+1


###按节奏输入文本
def input_text(string):
    '''
    string(str):文本
    interval(str):间隔
    '''
    for i in string:
        if os.name=='nt':
            os.system('D:\Downloads\scrcpy-win64-v2.1\\adb shell input text {}'.format(i))
        elif os.name=='posix':
            os.system('adb shell input text {}'.format(i))
#        time.sleep(float(interval))

###检查某个app是否在后台运行
def check_running(d,name):
    '''
    d(obj):u2连接对象
    name(str):app名称
    '''
    running_apps=d.app_list_running()
#    print(running_apps)
    for app in running_apps:
#        print(f'正在比对{app}')
        if name==app:
            return True

###自动逆回购
def reverse_repo(d,mode=0):
    '''
    d(obj):u2连接对象
    mode(int):0-测试模式，1-实战模式
    '''
    d(text="逆回购").click()
    d(text="R-001").click()
    d(text="借出").click()
    d(text="全仓").click()
    d(text="借出")[1].click()
    if mode==1:
        d(resourceId="com.xueqiu.android:id/tv_right").click()#确定
        print(f'正在逆回购')
        d(text="确定").click()
    elif mode==0:
        d(resourceId="com.xueqiu.android:id/tv_left").click()#取消
        print(f'测试逆回购')
#    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].clear_text()
#    d(resourceId="com.xueqiu.android:id/order_input_editText")[1].set_text(number)
#    cash=account(d)['available'].replace(',','')
#    cash=float(cash)
#    cash=int(cash/100)#100的整数倍
#    print(f'正在进行逆回购sz131810,金额{cash}')
#    sell(d,'SZ131810',cash)




###主程序
if __name__=='__main__':
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
