
#coding=utf8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
#from sqlalchemy import create_engine 
from stock_online import Initial

def plot():
#    sql="SELECT DISTINCT ts_code, ma"+str(mas)+",close"+" FROM Monthly ORDER BY trade_date DESC;" #构建SQL查询语句
    sql='SELECT DISTINCT ts_code,trade_date,ma13 FROM Monthly WHERE ts_code="000056.sz" ORDER BY trade_date DESC;' #构建SQL查询语句
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    plt.plot(df['trade_date'],df['ma13'])
#    plt.plot(data['trade_date'],data['ma55'])
    plt.show()

def new_plot(stock_code,freq,start,end,ma):#在线查询
    '''
    stock_code(str):股票代码
    freq(str):日，周，月
    start,end (str): 开始结束时间,如20230510
    ma (int):均线参数
    '''
    pro=Initial()
    data=ts.pro_bar(ts_code=stock_code,freq=freq,adj='qfq',start_date=start,end_date=end,ma=[ma])
    data=data.sort_index(axis=0,ascending=False)
    print(data)
    plt.plot(data['trade_date'],data[f'ma{ma}'])
    plt.show()
    

if __name__ == "__main__":
#    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/stock?charset=utf8&use_unicode=1') ##数据库初始化
#    plot()
    new_plot('002866.sz','D','20230101','20230511',13)
