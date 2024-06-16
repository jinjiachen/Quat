#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2023-11-24
'''

import urllib
import requests
import os,re,time
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


###模拟get，post请求
def general(method,url,data=''):
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
        #以下是获取cookie的尝试
#        print([x.__dict__ for x in s.cookies])
#        print(res.cookies)
#        print(s.cookies)
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
        #下面两条为抓取的实际示例
#        data_buy = "stockName=&stockCode=159601&exchange=SZ&securityType=3&price=0.686&num=4600&entrustType=1&channel=&deviceInfo="
#       data_sell="stockName=%E6%81%92%E7%94%9F%E4%BA%92%E8%81%94%E7%BD%91ETF&stockCode=513330&exchange=SH&securityType=3&price=0.370&num=100&entrustType=2&channel=&deviceInfo="

#        res=requests.post(buy_url,headers=myheader,data=data1)
        res=s.post(buy_url,headers=myheader,data=data)
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
        status=item.xpath('./div[2]/div/p[2]/text()')
        print(code,act,details,status)



###下单
def myorder(act,data):
    if act=='buy':
        buy_url='https://m.touker.com/trading/securitiesEntrust.json'
    elif act=='sell':
        sel_url=''
    general('post',data)

###菜单
def Menu():
    choice=input('pos:position\nlscj:历史成交\njrcj:今日成交\nact.帐户信息\njrwt:今日委托\nt:做T')
    if choice=='pos':
#        position_url=f'https://m.touker.com/trading/trade/trading-sub/position?_=1701162501444'#构建get请求的地址
        positions=get_position()
        for i,stock in enumerate(positions):
            print(f'{i+1}-->{stock}')
    elif choice=='lscj':
        consult('lscj')
    elif choice=='jrcj':
        consult('jrcj')
    elif choice=='act':
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
        code=input('请输入股票代码')
        price=input('请输入价格')
        amount=input('请输入数量')
        order('BUY','',code,price,amount)
    elif choice=='sell':
        code=input('请输入股票代码')
        price=input('请输入价格')
        amount=input('请输入数量')
        order('SELL','',code,price,amount)
    elif choice=='jrwt':
        consult('jrwt')
    elif choice=='t':
        code=input('请输入股票代码')
        price1=input('请输入价格1')
        price2=input('请输入价格2')
        amount=input('请输入数量')
        trade_T(code,price1,price2,amount)
    elif choice=='revoke':
        code=input('请输入股票代码')
        revoke(code)


###构建买卖的股票基本信息并下单
def order(act,stock_name,code,price,amount):
    '''
    act(str):买卖
    stock_name(str):股票名称
    code(str):代码
    price(float):价格
    amount(int):数量
    '''
    #基于股票代码,判断市场类型
    words_sh=['sh','XSHG']
    words_sz=['sz','XSHG','XSHE']
    if any(suffix in code for suffix in words_sh):
        market='SH'
#        print('市场为',market)
    elif any(suffix in code for suffix in words_sz):
        market='SZ'
#        print('市场为',market)
    #提取code中的数字部分
    code=re.search('\d+',code).group()
    #这个信息中包含了buy/sell的动作,1:buy,2:sell
    if act=='BUY':
        url='https://m.touker.com/trading/securitiesEntrust.json'
        data = f"stockName={stock_name}&stockCode={code}&exchange={market}&securityType=3&price={price}&num={amount}&entrustType=1&channel=&deviceInfo="
    elif act=='SELL':
        url='https://m.touker.com/trading/securitiesEntrust.json'
        data = f"stockName={stock_name}&stockCode={code}&exchange={market}&securityType=3&price={price}&num={amount}&entrustType=2&channel=&deviceInfo="
        
    print(data)
    general('post',url,data)


###保持登录状态
def keep_login():
    url='https://m.touker.com/trading/whetherNeedValidatePwd.json'
    res=requests.post(url)
    print(res.status_code)
    print(res.text)
    url_unreadmsg='https://m.touker.com/trading/queryUnReadMessageCount.json?channel=null&_=1718437688080'
    res=requests.post(url_unreadmsg)
    print(res.status_code)
    print(res.text)



def check_status():
    while True:
        keep_login()
        time.sleep(2)
    
###高买高卖做T
def trade_T(code,price1,price2,amount):
    '''
    code(str):股票代码
    price1(float):股价
    price2(float):股价
    amount:(int):股票数量
    '''
#def order(act,stock_name,code,price,amount):
    price_up=max(price1,price2)
    price_down=min(price1,price2)
    order('BUY','',code,price_down,amount)
    order('SELL','',code,price_up,amount)

###撤回委托
def revoke(code):
    conf=load_config()#读取配置文件
    s=requests.Session()
    hb_cookie=conf.get('hb','cookie')#获取配置文件中的cookie
    hb_cookie=base64.b64decode(hb_cookie).decode('ascii')
    myheader={
            'cookie':hb_cookie,
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br,zstd',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://m.touker.com',
            'Priority':'u=1,i',
            'referer': 'https://m.touker.com/trading/trade/revoke',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            }
    #基于股票代码,判断市场类型
    words_sh=['sh','XSHG']
    words_sz=['sz','XSHG','XSHE']
    if any(suffix in code for suffix in words_sh):
        market='SH'
#        print('市场为',market)
    elif any(suffix in code for suffix in words_sz):
        market='SZ'
#        print('市场为',market)
    #提取code中的数字部分
    code=re.search('\d+',code).group()
    url='https://m.touker.com/trading/revokeCommit.json'
    entrustcode=input('请输入信任代码')
    data=f'exchange={market}&stockCode={code}&entrustCode={entrustcode}'
    res=s.post(url,headers=myheader,data=data)
    print(data)
    print(res.status_code)
#    general('post',url,data)

if __name__=='__main__':
    Menu()
