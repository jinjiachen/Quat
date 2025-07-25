#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2023-11-24
'''

import urllib
import requests
import os,re,time,math,random
import base64,json
import easyquotation
from lxml import etree
from configparser import ConfigParser
from function import get_code_ts
from notification import notify


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
#        print(res.status_code)
#        print(res.url)
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
    deals=[]#保存最终的结果
    for item in items:
        cache=[]#保存每一次交易的结果
        code=item.xpath('./div/p/text()')
        act=item.xpath('./div[2]/button/text()')
        details=item.xpath('./div[2]/div/div/p/span/text()')
        status=item.xpath('./div[2]/div/p[2]/text()')
        [cache.append(i) for i in code]
        [cache.append(i) for i in act]
        [cache.append(i) for i in details]
        [cache.append(i) for i in status]
        deals.append(cache)
        print(code,act,details,status)
#    print(deals)
    return deals



###下单
def myorder(act,data):
    if act=='buy':
        buy_url='https://m.touker.com/trading/securitiesEntrust.json'
    elif act=='sell':
        sel_url=''
    general('post',data)

###菜单
def Menu():
    choice=input('ap:acount & position\npos:position\nlscj:历史成交\njrcj:今日成交\nact.帐户信息\njrwt:今日委托\nt:做T\nbuys:等权重买入一组股票\nsells:清仓列明表中持有的股票\nsync:同步jq组合\ncs:检查状态')
    if choice=='ap':
        base_info=get_account()
        print(base_info)
        positions=get_position()
        for i,stock in enumerate(positions):
            print(f'{i+1}-->{stock}')
        pass
    elif choice=='pos':
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
    elif choice=='buys':
        file_path=input('请输入文件路径:')
        total_cash=input('请输入买入股票的总金额:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        stocklist=get_code_ts(file_path)
        order_list('BUY',stocklist,float(total_cash),'YES')
    elif choice=='sells':
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        stocklist=get_code_ts(file_path)
        order_list('SELL',stocklist,100000,'YES')
    elif choice=='sync':
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        sync_jq(file_path,'YES')
    elif choice=='cs':
        check_status()



###构建买卖的股票基本信息并下单
def order(act,stock_name,code,price,amount):
    '''
    act(str):买卖
    stock_name(str):股票名称,可以为空
    code(str):代码
    price(float):价格
    amount(int):数量
    '''
    #基于股票代码,判断市场类型
    words_sh=['SH','sh','XSHG']
    words_sz=['SZ','sz','XSHE']
    if any(suffix in code for suffix in words_sh):
        market='SH'
#        print('市场为',market)
    elif any(suffix in code for suffix in words_sz):
        market='SZ'
#        print('市场为',market)
    #提取code中的数字部分
    code=re.search(r'\d+',code).group()
    #这个信息中包含了buy/sell的动作,1:buy,2:sell
    if act=='BUY':
        url='https://m.touker.com/trading/securitiesEntrust.json'
        data = f"stockName={stock_name}&stockCode={code}&exchange={market}&securityType=3&price={price}&num={amount}&entrustType=1&channel=&deviceInfo="
    elif act=='SELL':
        url='https://m.touker.com/trading/securitiesEntrust.json'
        data = f"stockName={stock_name}&stockCode={code}&exchange={market}&securityType=3&price={price}&num={amount}&entrustType=2&channel=&deviceInfo="
        
    print(data)
    general('post',url,data)

###等权重买入一组股票列表或者清仓列表中持有的股票
def order_list(act,stocklist,total_cash,ptf='NO'):
    '''
    act(str):买卖
    stocklist(litst):一组股票列表代码
    total_cash(float):总现金额
    ptf(str):是否输出信息
    '''
    quotation=easyquotation.use('sina')
    slip_pct=0.01#滑点百分比
    slip=0.95#固定滑点
    numbers=len(stocklist)#一组股票的数量
    cash=total_cash/numbers#均分到每只股票上的购买额
    amount=None#股票数量，默认为空
    if act=='SELL':#如果是卖出，需要用到持仓信息
        positions=get_position()#获取持仓
    
    #遍历每只股票，查询价格并计算购买数量
    for stock_code in stocklist:
        stock_info=quotation.real(stock_code[:6])#查询股票的价格信息,easyquotation查股票只要6位数字
        now=stock_info[stock_code[:6]]['now']#当前价格
        if act=='BUY':
            price=now*(1+slip_pct)#买入价比当前价高，便于买入
            price=round(price,2)
#            amount=math.floor(cash/price)#股票数量向下取整
            amount=cash/price//100#股票数量对100取整,可以理解为一手
            amount=max(amount*100,100)#股票最小为100
        elif act=='SELL':
            price=now*(1-slip_pct)#卖出价比当前价低，便于卖出
            price=round(price,2)
            #遍历每个持仓，比对所要卖出的股票是否在持仓中，如在，获取可卖数量
            for pos in positions:
                if stock_code==pos[1]:#pos[1]为股票代码
                    amount=pos[6]#pos[6]为股票数量
            if amount==None:
                print(f'{stock_code}不在持仓中')
        if amount!=None:
            order(act,'',stock_code,price,amount)
            if ptf=='YES':#调试用
                if act=='BUY':
                    print(f'总资金{total_cash},股票总数{numbers},每只股票金额{cash},正在{act} {stock_code},委托价格{price},数量{amount}')
                elif act=='SELL':
                    print(f'正在{act} {stock_code},委托价格{price},数量{amount}')

###同步jq组合的持仓
def sync_jq(file_path,ptf='NO'):
    '''
    file_path(str):jq持仓信息的文件路径
    '''
    #读取文件内容
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()

    #提取文件中的股票和数量信息
    codes_jq=[]
    nums_jq=[]
    for line in res:
        code_jq=re.search(r'\d{6}.XSH[GE]',line).group()#用正则提取股票代码
        num_jq=re.search(r'\d+股',line).group()
        num_jq=num_jq.replace('股','')
        if 'XSHE' in code_jq:
            code_jq=code_jq[:6]+'.SZ'#转换成tushare,hb代码
        elif 'XSHG' in code_jq:
            code_jq=code_jq[:6]+'.SH'#转换成tushare,hb代码
        codes_jq.append(code_jq)
        nums_jq.append(num_jq)
        if ptf=='YES':
            print(f'从文件中提取的股票:{code_jq},对应的数量:{num_jq}')

    #获取持仓信息，和文件内容进行比对
    positions=get_position()#获取持仓
    final_num=[]
    for code,num in zip(codes_jq,nums_jq):
        amount=None#数量初始化为空
        for pos in positions:
            if code==pos[1]:#比较股票代码，判断是否有持仓pos[1]为股票代码
                amount=int(num)-int(pos[6])#如果有持仓,比较jq和hb的数量差pos[6]为股票数量
                break
        if amount==None:
            final_num.append(num)
        else:
            final_num.append(amount)
    if ptf=='YES':
        for code,num in zip(codes_jq,final_num):
            print(f'比较后的股票:{code},数量:{num}')

    #实际交易
    slip_pct=0.01#滑点百分比
    slip=0.95#固定滑点
    quotation=easyquotation.use('sina')
    for code,num in zip(codes_jq,final_num):
        stock_info=quotation.real(code[:6])#查询股票的价格信息,easyquotation查股票只要6位数字
        now=stock_info[code[:6]]['now']#当前价格
        if num==0:
            if ptf=='YES':
                print(f'{code}数量为0，不做买卖')
            pass#占位用，防止程序出错
        elif '-' in str(num):#卖出
#            num=num.replace('-','')
            num=abs(num)
            price=now*(1-slip_pct)#卖出价比当前价低，便于卖出
            price=round(price,2)
#            order('SELL','',code,price,num)
            if ptf=='YES':
                print(f'正在卖出股票{code},价格:{price},数量:{num}')
        else:#买入
            price=now*(1+slip_pct)#买入价比当前价高，便于买入
            price=round(price,2)
#            order('BUY','',code,price,num)
            if ptf=='YES':
                print(f'正在买入股票{code},价格:{price},数量:{num}')
    



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
#        keep_login()
        now=time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            consult('jrcj')
            print('当前时间：',now)
            time.sleep(random.randint(180,240))#3-4分钟内随机
        except:
            print(f'server stopped at {now}')
#            notify('post','HB status',f'server stopped at {now}')
    
###高买高卖做T
def trade_T(code,price1,price2,amount,direction=None):
    '''
    code(str):股票代码
    price1(float):股价
    price2(float):股价
    amount:(int):股票数量
    '''
    price_up=max(price1,price2)
    price_down=min(price1,price2)
    if direction=='up':
        pass
    elif direction=='down':
        pass
    else:
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
    code=re.search(r'\d+',code).group()
    url='https://m.touker.com/trading/revokeCommit.json'
    entrustcode=input('请输入信任代码')
    data=f'exchange={market}&stockCode={code}&entrustCode={entrustcode}'
    res=s.post(url,headers=myheader,data=data)
    print(data)
    print(res.status_code)
#    general('post',url,data)

if __name__=='__main__':
    Menu()
