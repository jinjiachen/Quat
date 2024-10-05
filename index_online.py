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
from scipy.stats import percentileofscore


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
    #上证
    PEttm000001=index_percent(pro,'000001.sh','PE_ttm')
    PB000001=index_percent(pro,'000001.sh','PB')
    #深成
    PEttm399001=index_percent(pro,'399001.sz','PE_ttm')
    PB399001=index_percent(pro,'399001.sz','PB')
    if ptf=='YES':
        print('上证PE：',pe_sh)
        print('深证PE：',pe_sz)
        print('成交量：',amount[0])
        print('上证涨幅：',df_sh['pct_chg'][0])
        print('深证涨幅：',df_sz['pct_chg'][0])
    return {'amount':amount[0],\
            'pct_sh':df_sh['pct_chg'][0],\
            'pct_sz':df_sz['pct_chg'][0],\
            'pe_sh':pe_sh.values[0],\
            'pe_sz':pe_sz.values[0],\
            'PEttm000001':PEttm000001,\
            'PB000001':PB000001,\
            'PEttm399001':PEttm399001,\
            'PB399001':PB399001,
        }


###通过easyquotation获取实时指数涨跌幅和成交量
def live_index():
    quo=easyquotation.use('sina')
    stocklist=['sh000001','sz399001','sz399006','sh000016','sh000852','sh000905']
    res=quo.stocks(stocklist)
    #计算总成交量
    total_vol=(res['000001']['volume']+res['399001']['volume'])/10**8#两市总成交量,单位亿
    total_vol=round(total_vol,1)#圆整

    #计算涨跌幅
    sh=res['000001']['now']
    sh_pct=(res['000001']['now']/res['000001']['close']-1)*100#计算上证涨跌幅
    sh_pct=round(sh_pct,2)#圆整
    sh50=res['000016']['now']
    sh50_pct=(res['000016']['now']/res['000016']['close']-1)*100#计算上证50涨跌幅
    sh50_pct=round(sh50_pct,2)#圆整
    sz=res['399001']['now']
    sz_pct=(res['399001']['now']/res['399001']['close']-1)*100#计算深成涨跌幅
    sz_pct=round(sz_pct,2)#圆整
    cyb=res['399006']['now']
    cyb_pct=(res['399006']['now']/res['399006']['close']-1)*100#计算创业板涨跌幅
    cyb_pct=round(cyb_pct,2)#圆整
    zz1000=res['000852']['now']
    zz1000_pct=(res['000852']['now']/res['000852']['close']-1)*100#计算中证1000涨跌幅
    zz1000_pct=round(zz1000_pct,2)#圆整
    zz500=res['000905']['now']
    zz500_pct=(res['000905']['now']/res['000905']['close']-1)*100#计算中证500涨跌幅
    zz500_pct=round(zz500_pct,2)#圆整
    return {'total_vol':total_vol,
            'sh':sh,
            'sh_pct':sh_pct,
            'sz':sz,
            'sz_pct':sz_pct,
            'cyb':cyb,
            'cyb_pct':cyb_pct,
            'sh50':sh50,
            'sh50_pct':sh50_pct,
            'zz1000':zz1000,
            'zz1000_pct':zz1000_pct,
            'zz500':zz500,
            'zz500_pct':zz500_pct,
            }


###查询指数基本信息
def index_info(pro):
    df_index=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,pe,pe_ttm,pb')#查询指数信息
    pe_000001sh=df_index[df_index['ts_code']=='000001.SH']['pe']#上证PE
    pettm_000001sh=df_index[df_index['ts_code']=='000001.SH']['pe_ttm']#上证PE_TTM
    pb_000001sh=df_index[df_index['ts_code']=='000001.SH']['pb']#上证PB


###查询PE百分数
def index_percent(pro,index,style,ptf='NO'):
    '''
    pro(obj):tushare的对象
    index(str):指数的代码
    style(str):PB,PE,PE_ttm,total_mv
    '''
    now=time.strftime("%Y%m%d") #当前日期
#    now='20230914'
    previous=str(int(now)-100000)#换算到10年前
    df_now=pro.index_dailybasic(ts_code=index,trade_date=now, fields='ts_code,trade_date,pe,pe_ttm,pb,total_mv')#查询指数信息
    df_index=pro.index_dailybasic(ts_code=index,start_date=previous,end_date=now, fields='ts_code,trade_date,pe,pe_ttm,pb,total_mv')#查询指数信息
    if style=='PB':
        pb=df_now['pb'][0]
        pb_range=df_index['pb']
        percent=percentileofscore(pb_range,pb)
        percent=round(percent,2)
        return [pb,percent]
        if ptf=='YES':
            print('PB:',pb)
    elif style=='PE':
        pe=df_now['pe'][0]
        pe_range=df_index['pe']
        percent=percentileofscore(pe_range,pe)
        percent=round(percent,2)
        return [pe,percent]
        if ptf=='YES':
            print('PE:',pe)
    elif style=='PE_ttm':
        pe=df_now['pe_ttm'][0]
        pe_range=df_index['pe_ttm']
        percent=percentileofscore(pe_range,pe)
        percent=round(percent,2)
        return [pe,percent]
        if ptf=='YES':
            print('PE_ttm:',pe)
    elif style=='total_mv':
        total_mv=df_now['total_mv'][0]
        total_mv_range=df_index['total_mv']
        percent=percentileofscore(total_mv,total_mv)
        percent=round(percent,2)
        return [total_mv,percent]
        if ptf=='YES':
            print('total_mv:',total_mv)





###主程序
if __name__=='__main__':
    pro=Initial()
    res=statistics(pro)
    for key in res.keys():
        print(res[key])
