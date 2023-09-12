#coding=utf8
'''
author: Michael Jin
date: 2023-08-15
'''

import tushare as ts
import pandas as pd
import numpy as np
import time
import easyquotation
from stock_online import Initial


###统计沪深两大指数的涨跌幅和成交量
def statistics(pro,date='',ptf='NO'):
    if date=='':
        now=time.strftime("%Y%m%d") #当前日期
    else:
        now=date
    df_sh=pro.index_daily(ts_code='000001.SH',trade_date=now,fields='pct_chg,amount')
    df_sz=pro.index_daily(ts_code='399001.SZ',trade_date=now,fields='pct_chg,amount')
    amount=(df_sh['amount']+df_sz['amount'])/10**5#上证深证总交易额（亿元）

    df_index=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,pe')#查询指数pe
    pe_sh=df_index[df_index['ts_code']=='000001.SH']['pe']#上证PE
    pe_sz=df_index[df_index['ts_code']=='399001.SZ']['pe']#深成PE
    if ptf=='YES':
        print('上证PE：',pe_sh)
        print('深证PE：',pe_sz)
        print('成交量：',amount[0])
        print('上证涨幅：',df_sh['pct_chg'][0])
        print('深证涨幅：',df_sz['pct_chg'][0])
    return {'amount':amount[0],'pct_sh':df_sh['pct_chg'][0],'pct_sz':df_sz['pct_chg'][0],'pe_sh':pe_sh.values[0],'pe_sz':pe_sz.values[0]}


###通过easyquotation获取实时指数涨跌幅和成交量
def live_index():
    quo=easyquotation.use('sina')
    stocklist=['sh000001','sz399001','sz399006','sh000016','sh000852','sh000905']
    res=quo.stocks(stocklist)
    #计算总成交量
    total_vol=(res['000001']['volume']+res['399001']['volume'])/10**8#两市总成交量,单位亿
    total_vol=round(total_vol,1)#圆整

    #计算成交量
    sh_pct=(res['000001']['now']/res['000001']['close']-1)*100#计算上证涨跌幅
    sh_pct=round(sh_pct,2)#圆整
    sh50_pct=(res['000016']['now']/res['000016']['close']-1)*100#计算上证50涨跌幅
    sh50_pct=round(sh50_pct,2)#圆整
    sz_pct=(res['399001']['now']/res['399001']['close']-1)*100#计算深成涨跌幅
    sz_pct=round(sz_pct,2)#圆整
    cyb_pct=(res['399006']['now']/res['399006']['close']-1)*100#计算创业板涨跌幅
    cyb_pct=round(cyb_pct,2)#圆整
    zz1000_pct=(res['000852']['now']/res['000852']['close']-1)*100#计算中证1000涨跌幅
    zz1000_pct=round(zz1000_pct,2)#圆整
    zz500_pct=(res['000905']['now']/res['000905']['close']-1)*100#计算中证1000涨跌幅
    zz500_pct=round(zz500_pct,2)#圆整
    return {'total_vol':total_vol,
            'sh_pct':sh_pct,
            'sz_pct':sz_pct,
            'cyb_pct':cyb_pct,
            'sh50':sh50_pct,
            'zz1000':zz1000_pct,
            'zz500':zz500_pct,
            }


###主程序
if __name__=='__main__':
    pro=Initial()
    res=statistics(pro)
    for key in res.keys():
        print(res[key])
