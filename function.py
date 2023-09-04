#coding=utf8
import pandas as pd
import numpy as np
import easyquotation
import tushare as ts
import os
import time

def Average(data,ma,length): #输入单个股票的行情数据，返回对应均线数据
    '''
    data:行情数据
    ma:均线
    length:返回数据的个数
    '''
    a=[]
    i=1
    j=0
    while i<=max(ma,length+1): #每次计算一个均值，循环计算多次,循环次数为均线或周期中较大者,length+1是余量
        a.append(data.shift(j)[0:ma].fillna(0).mean()) #j为位移值，每次循环后数据向上位移，计算前一日的均值
#        a.append(data.shift(j)[0:ma].mean()) #j为位移值，每次循环后数据向上位移，计算前一日的均值
        i=i+1
        j=j-1

    for k in a:
        if k==0:
            return None
            break
    return a

def Str_Float(data):
    a=[]
    for i in data:
        a.append(float(i))
    return pd.Series(a)

def Qfq(data,factor):
    data=Str_Float(data)
    factor=Str_Float(factor)
    a=[]
    for i in factor:
        a.append(factor[0]) #构建一个数列，其值为最新一天的复权因子
    f=pd.Series(a)
    return data*factor/f #未复权值×对应日期的复权因子/最新一天的复权因子

def Split_line(words,figure): #分割线
    if figure=='=':
        print('='*20+words+'='*20)
    elif figure=='-':
        print('-'*20+words+'-'*20)
    elif figure=='*':
        print('*'*20+words+'*'*20)

#def FenHong(previous,post): #比较两个时间段间复权因子的变化，间接查找分红的股票

def cal_pct(stock_code):#计算单个股票涨跌幅
    '''
    stock_code:股票代码
    '''
    quotation=easyquotation.use('sina')
    stock_info=quotation.real(stock_code)#查询股票的价格信息
    close=stock_info[stock_code]['close']#昨日收盘价
    now=stock_info[stock_code]['now']#当前价格
    pct=round((now/close-1)*100,2)#计算涨跌幅
    return pct


def cal_pcts(stock_list):#计算一组股票的涨跌幅
    '''
    stock_list:股票代码的列表
    '''
    pcts=[]
    for stock in stock_list:
        pcts.append(cal_pct(stock[2:]))#对tushare股票代码进行处理，保留数字部分
    return pcts


def range_pcts(pro,stock_list,start,end):#计算一个时间段内的涨跌幅
    '''
    stock_list:一组股票代码
    start:开始时间:20090101
    end:结束时间:20090102
    '''
    pcts=[]
    for stock_code in stock_list:
        while True:
            try:
                df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start, end_date=end)
                break
            except IOError as e:
                print(f'{e},正在重试')
                continue
        value_end=df['close'][0]#区间终点的股价
        value_start=df['close'][len(df)-1]#区间起点的股价
#        print('start',value_start)
#        print('end',value_end)
        pct=round((value_end/value_start-1)*100,2)
        pcts.append(pct)
    return pcts

def average_pcts(pro,stock_list,start,end):#计算一段时间内的每一天的平均涨幅
    '''
    stock_list:一组股票代码
    start:开始时间:20090101
    end:结束时间:20090102
    '''
    ma_pcts=[]
    trade_date=pro.trade_cal(exchange='', start_date=start, end_date=end)
#    trade_date=trade_date.sort_index(axis=0,ascending=False)#降序排列，tushare日期由近及远，因此降序
#    print(trade_date)
    dates=list(range(0,len(trade_date)))
    dates.sort(reverse=True)
    print(dates)
    for index in dates:
#        print(trade_date['is_open'][index])
#        print(type(trade_date['is_open'][index]))
#        print(trade_date['is_open'][index]==1)
#        print(trade_date['cal_date'][index])
        if trade_date['is_open'][index]==1:#交易日
            to_date=trade_date['cal_date'][index]
            os.system('cls')
            print(f'正在比对{to_date}/{end}')
            pcts=range_pcts(pro,stock_list,start,to_date)
            ma_pcts.append(round(sum(pcts)/len(pcts),2))#计算平均值取2位小数
    return ma_pcts


def get_code(file_path):#提取致富代码
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
        stock_code=[] #构造空列表，用来存储股票代码
        for i in res:#遍历所有的结果
            stock_code.append(i.split('\t')[0])#提取结果中的致富代码
    return stock_code 


###查询当天是否已经更新
def is_updated(pro,content,date):
    '''
    pro:tushare的实例
    content(str):查询股票还是指数
    date(str):查询的日期
    '''
    if content=='stock':
        df=pro.daily(trade_date=date)
    elif content=='index':
        df=pro.index_daily(ts_code='000001.SH',trade_date=date)
    if len(df)==0:
        print(f'{date}数据未更新')
        return 'NO'
    elif len(df)>0:
        print(f'{date}数据已更新')
        return 'YES'


###定时运行指定函数
def schedule(func,to_go):
    '''
    func:函数名
    to_go(str):执行函数的时间
    '''
    while True:
        print('当前时间：',time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S")==to_go:
            print('go!!!')
            func()
            break


###计算指定路径下组合的涨跌幅
def pcts_list(path):
    '''
    path(str):股票文件的路径
    '''
    pcts=[]
    files=[f for f in os.listdir(path) if f.endswith('.txt')]#路径下的txt文件名
    file_path=[os.path.join(path, filename) for filename in files]#合并路径和文件名，形成文件绝对路径
    for txt in file_path:#遍历所有文件的绝对路径
        stocklist=get_code(txt)
        res=cal_pcts(stocklist)#每个股票的涨跌幅
        if len(res)!=0:
            pcts.append(sum(res)/len(res))#计算综合涨跌幅
        elif len(res)==0:
            pcts.append('NA')
    return[files,pcts]#返回文件名和对应的综合涨跌幅


###读取文件并提取股票代码，返回雪球格式的代码
def get_code(file_path):#提取致富代码
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
        stock_code=[] #构造空列表，用来存储股票代码
        for i in res:#遍历所有的结果
            stock_code.append(i.split('\t')[0].split('.')[1]+i.split('\t')[0].split('.')[0])#提取结果中的致富代码并作简单处理，如'sz000001'
    return stock_code 
