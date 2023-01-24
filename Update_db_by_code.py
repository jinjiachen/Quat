'''
Created on 2021年5月29日

@author: JJC

build the database from the beginning!!
'''
import pandas as pd
import tushare as ts
import time
import os
from sqlalchemy import create_engine 

db=input('Please input the database name:') #自定义数据库
engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/'+db+'?charset=utf8&use_unicode=1')

def Wait(n):
    i=0
    while i<n:
        i+=1

def Initial():#初始化
#    ts.set_token('3538f91058c1c4c9ceff9fd28ec1adea1981dc8d62d81a4606b13ecf') #jinjiachen_tux@163.com
    ts.set_token('7d2e85023208fe0be841215f20aa5e55ae1bb7a6cb23e459fd9ef56a') #13381598319
#    ts.set_token('3c8925948d2ff7d40a65155564ff30f87590ae40795bcefe7145a0fe') #709571784
    pro=ts.pro_api()
    return pro


def Stocklist():#从tushare获取股票列表
    sl=pro.stock_basic(exchange='',list_status='L',fields='ts_code')
    return sl


def get_basic_info(): #从tushare获取股票基本信息并写入到数据库中
    df=pro.stock_basic()
    res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)


def get_data(i,frequency): #从tushare获取单个股票的日/周/月线行情信息
    df=ts.pro_bar(ts_code=i,freq=frequency,adj='qfq',start_date=start,end_date=end,ma=[8,13,21,34,55,89,144,233])
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
        start=str(int(f.readline())+1) #从上次更新日期的后一天起更新
#        print(type(f.readline()))  #调试用
    end=time.strftime("%Y%m%d") #更新至当前日期

    get_basic_info() #调用函数

    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        print("更新数据库自"+str(start)+"至"+end) #打印更新的时间段
        for j in ['D','W','M']:
            df = get_data(i,j)
            Wait(90000)
            if df is not None: #查询结果为空，则还没有上市，不录入数据
                write_data(df,j)

    with open ('update_time.txt','w+') as f: #更新数据库结束，记录更新的日期
        f.write(end)
    f.close()
#    print(df)
