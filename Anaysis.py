#coding=utf8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine 
from stock_online import Initial


def sql_consult(db, date):
    sql="SELECT DISTINCT ts_code,trade_date,close FROM Daily WHERE trade_date="+date; #构建SQL查询语句
    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/'+db+'?charset=utf8&use_unicode=1') ##数据库初始化
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    return df


def pct_chg(period, start, end):
    close_start=sql_consult(db,start)
    close_end=sql_consult(db,end)

def PE(ts_code,start,end):
    pro=Initial()
    df=pro.daily_basic(ts_code=ts_code,start_date=start,end_date=end)
    df['pe']
    
def summary(file_path):
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
    print(res)
    for stock_info in res:
        splice=stock_info.split('\t')
