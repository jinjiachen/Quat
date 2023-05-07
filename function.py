#coding=utf8
import pandas as pd
import numpy as np
import easyquotation

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
