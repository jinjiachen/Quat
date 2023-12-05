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
                'X-Requested-Width':'XMLHttpRequest'
                }
        res=requests.get(url,headers=myheader)#发送get请求
        print(res.status_code)
        print(res.url)
#        print(res.text)
    elif method=='post':
        myheader={
#                'Accept':'text/html, */*; q=0.01',
#                'Accept-Encoding':'gzip, deflate, br',
#                'Accept-Language':'zh-CN,zh;q=0.9',
                'cookie':hb_cookie,
#                'Origin':'https://m.touker.com',
#                'Refer':'https://m.touker.com/trading/trade/buy',
#                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#                'X-Requested-Width':'XMLHttpRequest'
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
        data1 = "stockName=%E6%B2%AA%E6%B7%B1300ETF%E5%8D%8E%E5%A4%8F&stockCode=510330&exchange=SH&securityType=3&price=3.506&num=1100&entrustType=1&channel=&deviceInfo="
        res=requests.post(buy_url,headers=myheader,data=data1)
#        res=requests.post(buy_url,headers=myheader,data=data1,verify=False,allow_redirects=False)
        print(res.status_code)
#        print(data)
        print(res.text)

    return res

def Menu():
    choice=input('1.position\n2.历史成交\n3.今日成交\n4.帐户信息\n5.今日委托')
    if choice=='1':
#        position_url=f'https://m.touker.com/trading/trade/trading-sub/position?_=1701162501444'#构建get请求的地址
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
        for i,stock in enumerate(positions):
            print(f'{i+1}-->{stock}')
    elif choice=='2':
        consult_url='https://m.touker.com/trading/trade/entrustList?orderType=lscj'
        res=general('get',consult_url)
        selector=etree.HTML(res.text)
        items=selector.xpath('//div[@class="revoke-area"]/a')
#        print(items)
        deals=[]
        for item in items:
            code=item.xpath('./div/p/text()')
            act=item.xpath('./div[2]/button/text()')
            details=item.xpath('./div[2]/div/div/p/span/text()')
            print(code,act,details)

    elif choice=='3':
        consult_url='https://m.touker.com/trading/trade/entrustList?orderType=jrcj'
        res=general('get',consult_url)
        selector=etree.HTML(res.text)
        items=selector.xpath('//div[@class="revoke-area"]/a')
        deals=[]
        for item in items:
            code=item.xpath('./div/p/text()')
            act=item.xpath('./div[2]/button/text()')
            details=item.xpath('./div[2]/div/div/p/span/text()')
            print(code,act,details)
    elif choice=='4':
        url='https://m.touker.com/trading/baseInfo.json?_=1701498696248'
        res=general('get',url)
        base_info=json.loads(res.text)
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
        consult_url='https://m.touker.com/trading/trade/entrustList?orderType=jrwt'
        res=general('get',consult_url)
        selector=etree.HTML(res.text)
        items=selector.xpath('//div[@class="revoke-area"]/a')
        deals=[]
        for item in items:
            code=item.xpath('./div/p/text()')
            act=item.xpath('./div[2]/button/text()')
            details=item.xpath('./div[2]/div/div/p/span/text()')
            print(code,act,details)


if __name__=='__main__':
    Menu()
    pass
