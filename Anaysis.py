#coding=utf8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from sqlalchemy import create_engine 
from stock_online import Initial


def sql_consult(db, date):
    sql="SELECT DISTINCT ts_code,trade_date,close FROM Daily WHERE trade_date="+date; #构建SQL查询语句
    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/'+db+'?charset=utf8&use_unicode=1') ##数据库初始化
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    return df


def pct_chg(period, start, end):
    close_start=sql_consult(db,start)
    close_end=sql_consult(db,end)

def financial_indictor(ts_code='',trade_date):
    pro=Initial()
    df=pro.daily_basic(ts_code='', trade_date=trade_date, fields='ts_code,trade_date,pe,pe_ttm,pb,dv_ratio,dv_ttm,turnover_rate')
    df['pe']
    
def summary(file_path):#对结果文件总结
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
#    print(res)
    ZB=0
    ZXB=0
    CYB=0
    KCB=0
    BJS=0
    SZ=0
    SH=0
    for stock_info in res:
        splice=stock_info.split('\t')
#        print(len(splice))
        if len(splice)==8:
            if splice[5]=='主板':
                ZB+=1
                if 'SZ' in splice[0]:
                    SZ+=1
                elif 'SH' in splice[0]:
                    SH+=1
            elif splice[5]=='创业板':
                CYB+=1
            elif splice[5]=='科创板':
                KCB+=1
            elif splice[5]=='中小板':
                ZXB+=1
        elif len(splice)==6 and '北交所' in stock_info:
            BJS+=1

    result=f'主板：{ZB}(其中：上证{SH},深圳{SZ})\n中小板{ZXB}\n创业板：{CYB}\n科创板：{KCB}\n北交所：{BJS}\n总共：{len(res)}'
#    print(result)
    return result


def daily_push():
    now='20230524'
    df=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')
    pass

