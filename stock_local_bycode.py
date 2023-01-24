#coding=utf8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from sqlalchemy import create_engine 


def Stocklist():#获取股票列表
    sql="SELECT DISTINCT * FROM stock_basic"
    sl=pd.read_sql_query(sql, engine_ts)
    return sl
#    print(sl) #调试用


def Menu():
    print("请选择选股模型:")
    print("1.均线金叉模型")
    print("2.均线压制K线多时,K线站上均线模型")
    print("3.均线拐头模型")
    print("4.趋势模型")
    print("all:以上所有模型")
    choice=input()
    if choice=="1":
        freq=input("请输入均线周期:")
        mas=input("请输入短期均线:")
        mal=input("请输入长期均线:")
        n=input("请输入跨越的周期长度:")
        m=input("几天内金叉:")
        result=GoldenCross(freq,int(mas),int(mal),int(n),int(m))
        filename=freq+'cross'+mas+mal+'_'+n+'_'+m+'_'+now+'loc.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=="2":
        freq=input("请输入均线周期:")
        mas=input("请输入均线:")
        n=input("请输入跨越的周期长度:")
        m=input("K线在多长时间内站上均线:")
        result=Suppress(freq,int(mas),int(n),int(m))
        filename=freq+'suppress'+mas+'_'+n+"_"+m+'_'+now+'loc.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='3':
        freq=input("请输入均线周期:")
        ma_s=input("请输入均线:")
        n=input("请输入跨越的周期长度:")
        m=input("均线拐头天数:")
        result=Bottom(freq,int(ma_s),int(n),int(m))
        filename=freq+'bottom'+ma_s+'_'+n+"_"+m+'_'+now+'loc.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='4':
        freq=input("请输入均线周期:")
        ma_s=input("请输入均线:")
        n=input("均线趋势上扬时间:")
        result=Trend(freq,int(ma_s),int(n))
        filename=freq+'trend'+ma_s+'_'+n+'_'+now+'loc.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='all':
        print("正在设定均线金叉模型参数:")
        freq1=input("请输入均线周期:")
        mas=input("请输入短期均线:")
        mal=input("请输入长期均线:")
        n1=input("请输入跨越的周期长度:")
        result=Cross(freq1,int(mas),int(mal),int(n1))
        print("正在设定均均线压制K线多时,K线站上均线模型参数:")
        freq2=input("请输入均线周期:")
        n2=input("请输入跨越的周期长度:")
        result=Suppress(freq2,int(n2))

def SaveResult(filename,result):        
    with open ('/usr/local/src/tushare/result/'+filename,'w') as f:
        for i in result:
            details=StockDetails(i)
            for j in details:
                f.write(j)
            f.write('\n') 
        f.close()

def StockDetails(ts_code):
    details=[] #记录股票详细信息
    sql='SELECT * FROM stock_basic where ts_code="'+ts_code+'";' #构建SQL查询语句
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    for i in df.iloc[0]: #遍历DataFrame中的label:0
        details.append(i+'\t')
    return details


def GoldenCross(freq,mas,mal,n,m): #均线金叉
    print('调取数据库')
    if freq=="D":
        sql="SELECT DISTINCT ts_code, ma"+str(mas)+",ma"+str(mal)+" FROM Daily ORDER BY trade_date;" #构建SQL查询语句
    elif freq=="W":
        sql="SELECT ts_code, ma"+str(mas)+",ma"+str(mal)+" FROM Weekly;" #构建SQL查询语句
    elif freq=="M":
        sql="SELECT ts_code, ma"+str(mas)+",ma"+str(mal)+" FROM Monthly;" #构建SQL查询语句
    else:
        raise ValueError('查询周期错误')
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    print('完成调取数据库')
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=df[df['ts_code']==i] #运用布尔方法获取指定索引值，此处为获取指定股票代码的数据
#        print(data) #调试用
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma_s=data['ma'+str(mas)] #提取短期均线
        ma_l=data['ma'+str(mal)] #提取长期均线
        if len(ma_s)<n or len(ma_l)<n: #判断是否有空值
            continue
        if ma_s.iloc[0]>ma_l.iloc[0]: #判断短期均线是不是在长期均线上方
            j=1
            crosspoint=0 #初始值为0,假设1天内出现金叉的情况
            while j<=n: #判断之前的收盘价是不是在均线下文，以此寻找刚启动的行情
                if ma_s.iloc[j]>ma_l.iloc[j]: #判断短期均线是否还在长期均线上方，不是则交叉点已经出现
                    crosspoint=j #记录金叉时的天数
                    j=j+1
                else:
                    if crosspoint<=m: #判断交叉点是否在要求的时间段里,是则继续判断
                        j+=1
                        if j==n: #交叉前的N天，短期均线都在长期均线下方,可以断定为金叉
                            result.append(i)
                    else:
                        break
    print(result)
    return result

def Suppress(freq,mas,n,m): #K线站上均线模型
    print('调取数据库')
    if freq=="D":
        sql="SELECT DISTINCT ts_code, ma"+str(mas)+",close"+" FROM Daily ORDER BY trade_date DESC;" #构建SQL查询语句
    elif freq=="W":
        sql="SELECT DISTINCT ts_code, ma"+str(mas)+",close"+" FROM Weekly ORDER BY trade_date DESC;" #构建SQL查询语句
    elif freq=="M":
        sql="SELECT DISTINCT ts_code,trade_date, ma"+str(mas)+",close"+" FROM Monthly ORDER BY trade_date DESC;" #构建SQL查询语句
    else:
        raise ValueError('查询周期错误')
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    print('完成调取数据库')
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=df[df['ts_code']==i] #运用布尔方法获取指定索引值，此处为获取指定股票代码的数据
#        data.to_csv('/tmp/test.csv')
#        break
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        close=data['close']
        ma=data['ma'+str(mas)]
        if len(close)<n or len(ma)<n: #判断是否有空值
            continue
        if close.iloc[0]>ma.iloc[0]: #判断最新收盘价是不是在均线上方
            j=1
            point=0
            while j<=n: #判断之前的收盘价是不是在均线下文，以此寻找刚启动的行情
                if close.iloc[j]>ma.iloc[j]: #判断K线是否还在长期均线上方，不是则突破压制
                    point=j #记录突破时的天数
                    j=j+1
                else:
                    if point==m: #判断突破是否在要求的时间段里,是则继续判断
                        if j==n: #突破前的N段时间内，都在均线下方，突破成立
                            result.append(i)
                        j+=1
                    else:
                        break
    return result

def Trend(freq,ma_s,n): #单调递增模型
    print('调取数据库')
    if freq=="D":
        sql="SELECT ts_code, ma"+str(ma_s)+" FROM Daily;" #构建SQL查询语句
    elif freq=="W":
        sql="SELECT ts_code, ma"+str(ma_s)+" FROM Weekly;" #构建SQL查询语句
    elif freq=="M":
        sql="SELECT ts_code, ma"+str(ma_s)+" FROM Monthly;" #构建SQL查询语句
    else:
        raise ValueError('查询周期错误')
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    print('完成调取数据库')
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=df[df['ts_code']==i] #运用布尔方法获取指定索引值，此处为获取指定股票代码的数据
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma=data['ma'+str(ma_s)]
        if len(ma)<n: #判断是否有空值
            continue
        j=0 #循环初始化
        while ma.iloc[j]>ma.iloc[j+1]:
            if j==n: #n天内，均线单调递增
                result.append(i)
                break
            j+=1
    return result
                

def Bottom(freq,ma_s,n,m): #均线拐点
    print('调取数据库')
    if freq=="D":
        sql="SELECT DISTINCT ts_code, ma"+str(ma_s)+" FROM Daily ORDER BY trade_date ASC;" #构建SQL查询语句
    elif freq=="W":
        sql="SELECT DISTINCT ts_code, ma"+str(ma_s)+" FROM Weekly ORDER BY trade_date DESC;" #构建SQL查询语句
    elif freq=="M":
        sql="SELECT DISTINCT ts_code, ma"+str(ma_s)+" FROM Monthly ORDER BY trade_date DESC;" #构建SQL查询语句
    else:
        raise ValueError('查询周期错误')
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    print('完成调取数据库')
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=df[df['ts_code']==i] #运用布尔方法获取指定索引值，此处为获取指定股票代码的数据
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma=data['ma'+str(ma_s)] #提取均线
        if len(ma)<n: #判断是否有空值
            continue
        j=0 #初始化
        if ma.iloc[j]>ma.iloc[j+1]: #判断当前均值是否大于前一天，即均线拐头,如不是，则均线向下，不合要求，排除
            j=j+1
            while ma.iloc[j]>ma.iloc[j+1]: #向前递归，直到出现拐点
                j=j+1
            point=j #记录拐点
        else:
            continue
        if point==m: #拐点是否在要求的时间
            while ma.iloc[j]<=ma.iloc[j+1]: #向前递归，拐点前是否单调递减
                j=j+1
                if j==n: #直到规定的时间内，都是单调递减，则输出
                    result.append(i)
                    break #捕捉到致富代码，则退出循环，寻找下一个
    return result


####主程序####
if __name__ == '__main__':
    now=time.strftime("%Y%m%d") #当前日期
#    now='20220103'
    previous=int(now)-30000 #一年前的日期
    previous=str(previous) #转换成字符串
    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/tushare?charset=utf8&use_unicode=1') ##数据库初始化
#    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/bydate?charset=utf8&use_unicode=1') ##数据库初始化

###调用函数
    sl=Stocklist() #股票列表
#    sl=sl[100:400] #调试用，限制股票数量以减短时间
    Menu()



    #result=Cross('W',13,55,2) #调试用
    #result=Suppress('M',8,10) #调试用
    #result=GoldenCross('D',8,21,3,1) #调试用
    #result=Trend('W',55,100) #调试用
    #result=Bottom('M',21,12,2) #调试用
    #SaveResult('test',result) #调试用

