#coding=utf8
'''
author: Michael Jin
date: 2023-08-15
'''

import tushare as ts
import pandas as pd
import numpy as np
import time
from stock_online import Initial


###统计沪深两大指数的涨跌幅和成交量
def statistics(pro,ptf='NO'):
    now=time.strftime("%Y%m%d") #当前日期
    df_sh=pro.index_daily(ts_code='000001.SH',trade_date=now,fields='pct_chg,amount')
    df_sz=pro.index_daily(ts_code='399001.SZ',trade_date=now,fields='pct_chg,amount')
    amount=(df_sh['amount']+df_sz['amount'])/10**8#上证深证总交易额（千亿元）

    df_index=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,pe')#查询指数pe
    pe_sh=df_index[df_index['ts_code']=='000001.SH']['pe']#上证PE
    pe_sz=df_index[df_index['ts_code']=='399001.SZ']['pe']#深成PE
    if ptf=='YES':
        print('上证PE：',pe_sh)
        print('深证PE：',pe_sz)
    return {'amount':amount[0],'pct_sh':df_sh['pct_chg'][0],'pct_sz':df_sz['pct_chg'][0],'pe_sh':pe_sh[0],'pe_sz':pe_sz[0]}


###主程序
if __name__=='__main__':
    pro=Initial()
    res=statistics(pro)
    for key in res.keys():
        print(res[key])
