#coding=utf8
'''
author: Michael Jin
date: 20230919
'''
import tushare as ts
import pandas as pd
import numpy as np
from stock_online import Initial


###指定时间段内上市的基金,受限于账号积分，只能获取2015年之后的行情
def fund_new(pro,start,end):
    '''
    pro:tushare的实例对象
    start(int):开始时间
    end(int):结束时间
    '''
    #场内基金
    df_E=pro.fund_basic(market='E',status='L',fields='ts_code,name,found_date,list_date,issue_date,issue_amount')#场内上市的基金
    verdict=pd.to_numeric(df_E['list_date'])>=start
    df_tmp=df_E[verdict]
    verdict=pd.to_numeric(df_tmp['list_date'])<=end
    res_in=df_tmp[verdict]
    num_in=len(res_in['ts_code'])
    amount_in=res_in['issue_amount'].sum()
    #场外基金
    df_O=pro.fund_basic(market='O',status='L',fields='ts_code,name,found_date,list_date,issue_date,issue_amount')#场外上市的基金
    verdict=pd.to_numeric(df_O['found_date'])>=start
    df_tmp=df_O[verdict]
    verdict=pd.to_numeric(df_tmp['found_date'])<=end
    res_out=df_tmp[verdict]
    num_out=len(res_out['ts_code'])
    amount_out=res_out['issue_amount'].sum()
    return {
            'in':res_in,
            'num_in':num_in,
            'amount_in':amount_in,
            'out':res_out,
            'num_out':num_out,
            'amount_out':amount_out,
            }
