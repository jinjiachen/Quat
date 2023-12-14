#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2023-11-24
'''

import urllib
import requests
import os
import base64,json
from lxml import etree
from configparser import ConfigParser


def load_config():#加载配置文件
    conf=ConfigParser()
    if os.name=='nt':
#        path=r'.\config.ini'
        path=r'D:\Downloads\PortableGit-2.36.1-64-bit.7z\bin\Quat\config.ini'
    elif os.name=='posix':
        path='/usr/local/src/Quat/config.ini'
    else:
        print('no config file was found!')

    conf.read(path,encoding="utf-8")
    return conf


def general(method,url):
    '''
    功能：推送消息
    title:消息的标题
    content:消息的内容

    '''
    conf=load_config()#读取配置文件
    s=requests.Session()
    hb_cookie=conf.get('hb','cookie')#获取配置文件中的cookie
    hb_cookie=base64.b64decode(hb_cookie).decode('ascii')
#    print(type(hb_cookie))
#    print(hb_cookie)
#    hb_cookie=input('请输入cookie')

    if method=='get':
        myheader={
                'Accept':'text/html, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'cookie':hb_cookie,
                'Refer':'https://m.touker.com/trading/trade/position',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'X-Requested-Width':'XMLHttpRequest',
                'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Platform':'Windows',
                'Sec-Fetch-Dest':'document',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-Site':'same-origin',
                }
#        res=requests.get(url,headers=myheader,allow_redirects=False)#发送get请求
        res=s.get(url,headers=myheader,allow_redirects=False)#发送get请求
        print(res.status_code)
        print(res.url)
#        print([x.__dict__ for x in s.cookies])
        print(res.cookies)
        print(s.cookies)
#        print(res.text)
    elif method=='post':
        myheader={
                'cookie':hb_cookie,
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://m.touker.com',
                'referer': 'https://m.touker.com/trading/trade/buy',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Windows",
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'Host': 'm.touker.com'
                }
        buy_url='https://m.touker.com/trading/securitiesEntrust.json'
        data1 = "stockName=&stockCode=159601&exchange=SZ&securityType=3&price=0.686&num=4600&entrustType=1&channel=&deviceInfo="
#        res=requests.post(buy_url,headers=myheader,data=data1)
        res=s.post(buy_url,headers=myheader,data=data1)
        print(s.cookies)
#        res=requests.post(buy_url,headers=myheader,data=data1,verify=False,allow_redirects=False)
        print(res.status_code)
#        print(data)
        print(res.text)

    return res


###查询持仓
def get_position():
    position_url='https://m.touker.com/trading/queryHoldPosition.json?positionType=total&_=1701322363576'#持仓明细
    res=general('get',position_url)
    selector=etree.HTML(res.text)
    items=selector.xpath('//div[@class="position-item"]')
    positions=[]
    for item in items:
        total_info=[]
#            print(etree.tostring(item))
        part1=item.xpath('./div/div/div/text()')
        part2=item.xpath('./div/div/div/div/text()')
        total_info=part1[0:7]+part2
#            print(part1[0:7]+part2)
#            print('='*50)
        positions.append(total_info)
    return positions


###获取账户信息
def get_account():
    url='https://m.touker.com/trading/baseInfo.json?_=1701498696248'
    res=general('get',url)
    base_info=json.loads(res.text)
    return base_info


###查询委托成交
def consult(act):
    '''
    act(str):查询的动作，即历史委托(lswt)，今日委托(jswt),历史成交(lscj),今日成交(jrcj)等
    '''
    consult_url=f'https://m.touker.com/trading/trade/entrustList?orderType={act}'
    res=general('get',consult_url)
    selector=etree.HTML(res.text)
    items=selector.xpath('//div[@class="revoke-area"]/a')
    deals=[]
    for item in items:
        code=item.xpath('./div/p/text()')
        act=item.xpath('./div[2]/button/text()')
        details=item.xpath('./div[2]/div/div/p/span/text()')
        print(code,act,details)


###菜单
def Menu():
    choice=input('1.position\n2.历史成交\n3.今日成交\n4.帐户信息\n5.今日委托')
    if choice=='1':
#        position_url=f'https://m.touker.com/trading/trade/trading-sub/position?_=1701162501444'#构建get请求的地址
        positions=get_position()
        for i,stock in enumerate(positions):
            print(f'{i+1}-->{stock}')
    elif choice=='2':
        consult('lscj')
    elif choice=='3':
        consult('jrcj')
    elif choice=='4':
        base_info=get_account()
#        url='https://m.touker.com/trading/baseInfo.json?_=1701498696248'
#        res=general('get',url)
#        base_info=json.loads(res.text)
        print(base_info)
        assets=base_info['totalAssets']
        market_values=base_info['totalMarketValue']
        available=base_info['useAvailable']
        profits=base_info['totalHoldingProfit']
        today_profit=base_info['todayProfit']
#        print(assets,market_values,available,profits,today_profit)
    elif choice=='buy':
        general('post','')
    elif choice=='5':
        consult('jrwt')


###构建买卖的股票基本信息
def stk_info(stock_name,code,price,amount):
    '''
    stock_name(str):股票名称
    code(str):代码
    price(float):价格
    amount(int):数量
    '''
    res = "stockName={stock_name}&stockCode={code}&exchange={market}&securityType=3&price={price}&num={amount}&entrustType=1&channel=&deviceInfo="
    return res

if __name__=='__main__':
    Menu()
