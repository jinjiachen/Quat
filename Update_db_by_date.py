'''
Created on 2021年5月29日

@author: JJC

build the database from the beginning!!
'''
import pandas as pd
import tushare as ts
import time
import datetime 
import os
from sqlalchemy import create_engine 
import function
import pdb

db=input('Please input the database name:') #自定义数据库
engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/'+db+'?charset=utf8&use_unicode=1')

def Initial():#初始化
    ts.set_token('3538f91058c1c4c9ceff9fd28ec1adea1981dc8d62d81a4606b13ecf') #jinjiachen_tux@163.com
#    ts.set_token('3c8925948d2ff7d40a65155564ff30f87590ae40795bcefe7145a0fe') #709571784
#    ts.set_token('7d2e85023208fe0be841215f20aa5e55ae1bb7a6cb23e459fd9ef56a') #13381598319
#    ts.set_token('b71f6ca29a40085445c834192d29f73a132c238a590ea485570b76d4') #JYY QQ
    pro=ts.pro_api()
    return pro


def Stocklist():#从tushare获取股票列表
    sl=pro.stock_basic(exchange='',list_status='L',fields='ts_code')
    return sl


def get_basic_info(): #从tushare获取股票基本信息并写入到数据库中
    df=pro.stock_basic()
    res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)

def get_adj_factor(i): #从tushare获取股票复权因子并写入到数据库中
    df=pro.adj_factor(trade_date=i)
    res = df.to_sql('adj_factor', engine_ts, index=False, if_exists='append', chunksize=5000)

def get_data(i,frequency): #从tushare获取单个股票的日/周/月线行情信息
    if frequency=='D':
        df=pro.daily(trade_date=i)
    elif frequency=='W':
        df=pro.weekly(trade_date=i)
    elif frequency=='M':
        df=pro.monthly(trade_date=i)
    return df

def write_data(df,frequency): #配合get_data函数将获取的股票日/周/月行情信息写入到数据库中
    if frequency=='D':
        res = df.to_sql('Daily', engine_ts, index=False, if_exists='append', chunksize=5000)
    elif frequency=='W':
        res = df.to_sql('Weekly', engine_ts, index=False, if_exists='append', chunksize=5000)
    elif frequency=='M':
        res = df.to_sql('Monthly', engine_ts, index=False, if_exists='append', chunksize=5000)

if __name__ == '__main__':
    pro=Initial() #初始化
    sl=Stocklist() #股票列表
#    sl=sl[2401:2500] #调试用

    #更新数据库的起止时间
    with open ('update_time.txt','r') as f: #读取上次更新数据库的时间
        recordtime=f.readline() #读取的字符串会以\n结尾，在字符串比较时要特别注意
    f.close()

    now_time=datetime.datetime.now() #当前日期
    while(now_time.strftime("%Y%m%d")+'\n' != recordtime): #判断当前时间是否等于上次更新的时间，如果不是，往前递减，直到找到上次更新时间
        now_time=now_time+datetime.timedelta(days=-1) #往前递减
        print('last update time:'+recordtime)
        print('comparing:'+now_time.strftime("%Y%m%d"))
#        print(type(recordtime))  #调试用
        os.system('clear')
#        break
        trade_time=now_time+datetime.timedelta(days=+1) #从上次更新的时间后一天起开始更新
    function.Split_line('已找到上次更新日期'+recordtime[0:8]+'，开始更新','=') #添加分割线


    get_basic_info() #调用函数

#    while(trade_time.strftime("%Y%m%d") != time.strftime("%Y%m%d")): #当更新日期和当前日期不一致时，开始循环，知道更新日期等于当前日期
    while (trade_time.strftime("%Y%m%d") != (datetime.datetime.now()+datetime.timedelta(days=+1)).strftime("%Y%m%d")): #当更新日期和当前日期不一致时，开始循环，知道更新日期等于当前日期
#        pdb.set_trace()
        print('Updating:'+trade_time.strftime("%Y%m%d"))
        get_adj_factor(trade_time.strftime("%Y%m%d")) #获取复权因子
        for j in ['D','W','M']:
            df = get_data(trade_time.strftime("%Y%m%d"),j)
            if df is not None: #查询结果为空，则还没有上市，不录入数据
                write_data(df,j)
        trade_time=trade_time+datetime.timedelta(days=+1) #日期往后一天

    with open ('update_time.txt','w+') as f: #更新数据库结束，记录更新的日期
        f.write(trade_time.strftime("%Y%m%d"))
    f.close()
#    print(df)
