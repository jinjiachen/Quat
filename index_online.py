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
    previous=str(int(now)-100000)#换算到10年前
    df_sh=pro.index_daily(ts_code='000001.SH',start_date=previous,end_date=now,fields='close,pct_chg,amount')
    df_sz=pro.index_daily(ts_code='399001.SZ',start_date=previous,end_date=now,fields='close,pct_chg,amount')
    df_hs300=pro.index_daily(ts_code='000300.SH',start_date=previous,end_data=now,fields='close,pct_chg,amount')
    df_zz500=pro.index_daily(ts_code='000905.SH',start_date=previous,end_data=now,fields='close,pct_chg,amount')
    df_sz50=pro.index_daily(ts_code='000016.SH',start_date=previous,end_data=now,fields='close,pct_chg,amount')
    df_cyb=pro.index_daily(ts_code='399006.SZ',start_date=previous,end_data=now,fields='close,pct_chg,amount')
    amount=(df_sh['amount']+df_sz['amount'])/10**5#上证深证总交易额（亿元）

    df_index=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,pe')#查询指数pe
    pe_sh=df_index[df_index['ts_code']=='000001.SH']['pe']#上证PE
    pe_sz=df_index[df_index['ts_code']=='399001.SZ']['pe']#深成PE
    #上证
    PEttm000001=index_percent(pro,'000001.sh','PE_ttm')
    PB000001=index_percent(pro,'000001.sh','PB')
    price_now_000001=df_sh['close'][0]#当日收盘价
    price_range_000001=df_sh['close']#所有收盘价
    percent=percentileofscore(price_range_000001,price_now_000001)#计算收盘价百分比
    PP000001=round(percent,2)#PP=price percent
    #深成
    PEttm399001=index_percent(pro,'399001.sz','PE_ttm')
    PB399001=index_percent(pro,'399001.sz','PB')
    price_now_399001=df_sz['close'][0]#当日收盘价
    price_range_399001=df_sz['close']#所有收盘价
    percent=percentileofscore(price_range_399001,price_now_399001)#计算收盘价百分比
    PP399001=round(percent,2)#PP=price percent
    #沪深300
    PEttm000300=index_percent(pro,'000300.sh','PE_ttm')
    PB000300=index_percent(pro,'000300.sh','PB')
    price_now_000300=df_hs300['close'][0]#当日收盘价
    price_range_000300=df_hs300['close']#所有收盘价
    percent=percentileofscore(price_range_000300,price_now_000300)#计算收盘价百分比
    PP000300=round(percent,2)#PP=price percent
    #中证500
    PEttm000905=index_percent(pro,'000905.sh','PE_ttm')
    PB000905=index_percent(pro,'000905.sh','PB')
    price_now_000905=df_zz500['close'][0]#当日收盘价
    price_range_000905=df_zz500['close']#所有收盘价
    percent=percentileofscore(price_range_000905,price_now_000905)#计算收盘价百分比
    PP000905=round(percent,2)#PP=price percent
    #中证1000(暂无)
#    PEttm000852=index_percent(pro,'000852.sh','PE_ttm')
#    PB000852=index_percent(pro,'000852.sh','PB')
    #国证2000(暂无)
#    PEttm399303=index_percent(pro,'399303.sz','PE_ttm')
#    PB399303=index_percent(pro,'399303.sz','PB')
    #上证50
    PEttm000016=index_percent(pro,'000016.sh','PE_ttm')
    PB000016=index_percent(pro,'000016.sh','PB')
    price_now_000016=df_sz50['close'][0]#当日收盘价
    price_range_000016=df_sz50['close']#所有收盘价
    percent=percentileofscore(price_range_000016,price_now_000016)#计算收盘价百分比
    PP000016=round(percent,2)#PP=price percent
    #创业板
    PEttm399006=index_percent(pro,'399006.sz','PE_ttm')
    PB399006=index_percent(pro,'399006.sz','PB')
    price_now_399006=df_cyb['close'][0]#当日收盘价
    price_range_399006=df_cyb['close']#所有收盘价
    percent=percentileofscore(price_range_399006,price_now_399006)#计算收盘价百分比
    PP399006=round(percent,2)#PP=price percent
    if ptf=='YES':
        print('上证PE：',pe_sh)
        print('深证PE：',pe_sz)
        print('成交量：',amount[0])
        print('上证涨幅：',df_sh['pct_chg'][0])
        print('深证涨幅：',df_sz['pct_chg'][0])
    return {'amount':amount[0],\
            'pe_sh':pe_sh.values[0],\
            'pe_sz':pe_sz.values[0],\
            #上证
            'close_sh':df_sh['close'][0],\
            'pct_sh':df_sh['pct_chg'][0],\
            'PP000001':PP000001,\
            'PEttm000001':PEttm000001,\
            'PB000001':PB000001,\
            #深证
            'close_sz':df_sz['close'][0],\
            'pct_sz':df_sz['pct_chg'][0],\
            'PP399001':PP399001,\
            'PEttm399001':PEttm399001,\
            'PB399001':PB399001,
            #沪深300
            'close_hs300':df_hs300['close'][0],\
            'pct_hs300':df_hs300['pct_chg'][0],\
            'PP000300':PP000300,\
            'PEttm000300':PEttm000300,\
            'PB000300':PB000300,
            #中证500
            'close_zz500':df_zz500['close'][0],\
            'pct_zz500':df_zz500['pct_chg'][0],\
            'PP000905':PP000905,\
            'PEttm000905':PEttm000905,\
            'PB000905':PB000905,
#            'PEttm000852':PEttm000852,\
#            'PB000852':PB000852,
#            'PEttm399303':PEttm399303,\
#            'PB399303':PB399303,
            #上证50
            'close_sz50':df_sz50['close'][0],\
            'pct_sz50':df_sz50['pct_chg'][0],\
            'PP000016':PP000016,\
            'PEttm000016':PEttm000016,\
            'PB000016':PB000016,
            #创业板
            'close_cyb':df_cyb['close'][0],\
            'pct_cyb':df_cyb['pct_chg'][0],\
            'PP399006':PP399006,\
            'PEttm399006':PEttm399006,\
            'PB399006':PB399006,
        }


###通过easyquotation获取实时指数涨跌幅和成交量
def live_index():
    quo=easyquotation.use('sina')
    stocklist=['sh000001','sz399001','sz399006','sh000016','sh000852','sh000905','sh000300','sz399303']
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
    hs300=res['000300']['now']
    hs300_pct=(res['000300']['now']/res['000300']['close']-1)*100#计算沪深300涨跌幅
    hs300_pct=round(hs300_pct,2)#圆整
    gz2000=res['399303']['now']
    gz2000_pct=(res['399303']['now']/res['399303']['close']-1)*100#计算国证2000涨跌幅
    gz2000_pct=round(gz2000_pct,2)#圆整
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
            'hs300':hs300,
            'hs300_pct':hs300_pct,
            'gz2000':gz2000,
            'gz2000_pct':gz2000_pct,
            }


###查询指数基本信息
def index_info(pro):
    df_index=pro.index_dailybasic(trade_date=now, fields='ts_code,trade_date,pe,pe_ttm,pb')#查询指数信息
    pe_000001sh=df_index[df_index['ts_code']=='000001.SH']['pe']#上证PE
    pettm_000001sh=df_index[df_index['ts_code']=='000001.SH']['pe_ttm']#上证PE_TTM
    pb_000001sh=df_index[df_index['ts_code']=='000001.SH']['pb']#上证PB


###通过tushare查询PE百分数
def index_percent(pro,index,style,date='',ptf='NO'):
    '''
    pro(obj):tushare的对象
    index(str):指数的代码
    date(str):查询日期，如20240930
    style(str):PB,PE,PE_ttm,total_mv
    '''
    if date=='':
        now=time.strftime("%Y%m%d") #当前日期
    else:
        now=date
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
        percent=percentileofscore(total_mv_range,total_mv)
        percent=round(percent,2)
        return [total_mv,percent]
        if ptf=='YES':
            print('total_mv:',total_mv)


###通过tushare查询GDP
def consult_GDP(pro,date):
    '''
    pro(obj):tushare的对象
    date(str):查询日期，形如2023q1-2024q3
    '''
    q=date.split('-')
    df=pro.cn_gdp(start_q=q[0],end_q=q[1],fields='quarter,gdp,gdp_yoy')
    total=df['gdp'][0]/10**4 #总gdp,单位万亿
    return {'GDP':total,'data':df}

###通过tushare查询两市总市值
def consult_total_mv(pro,date,ptf='NO'):
    '''
    pro(obj):tushare的对象
    date(str):查询日期，形如20240930
    '''
    df=pro.index_dailybasic(trade_date=date, fields='ts_code,total_mv,turnover_rate,pe')
    mv_sh=df[df['ts_code']=='000001.SH']['total_mv']#上证的市值
    mv_sz=df[df['ts_code']=='399001.SZ']['total_mv']#深证的市值
    hs300=df[df['ts_code']=='000300.SH']['total_mv']#沪深300的市值
    total=(mv_sh.values[0]+mv_sz.values[0])/10**12#计算总市值，单位万亿
    if ptf=='YES':
        print(mv_sh)
        print(mv_sz)
        print(hs300)
        print(total)
    return total

###菜单
def Menu():
    choice=input('请选择功能：\n1.查询两市总市值\n2.查询GDP\n3.查询实时指数\n4.查询指数PE,PB,PE_ttm百分比')
    if choice=='1':
        date=input('请输入查询日期：')
        res=consult_total_mv(pro,date,ptf='YES')
    elif choice=='2':
        date=input('请输入查询日期(2024q1-2024q4)：')
        res=consult_GDP(pro,date)
        print(res)
    elif choice=='3':
        res=live_index()
#        print(res)
        print(f"上证：{res['sh']}-->{res['sh_pct']}")
        print(f"深证：{res['sz']}-->{res['sz_pct']}")
        print(f"沪深300：{res['hs300']}-->{res['hs300_pct']}")
        print(f"创业板：{res['cyb']}-->{res['cyb_pct']}")
        print(f"上证50：{res['sh50']}-->{res['sh50_pct']}")
        print(f"中证500：{res['zz500']}-->{res['zz500_pct']}")
        print(f"中证1000：{res['zz1000']}-->{res['zz1000_pct']}")
        print(f"国证2000：{res['gz2000']}-->{res['gz2000_pct']}")
    elif choice=='4':
        date=input('请输入查询日期：')
        index=input('请输入查询的指数(000001.sh)：')
        styles=['PE','PE_ttm','PB','total_mv']
        res={}
        for style in styles:
            res[style]=index_percent(pro,index,style,date,ptf='NO')
        print(res)




###主程序
if __name__=='__main__':
    pro=Initial()
    while True:
        Menu()
#    res=statistics(pro,date='20240930')
#    for key in res.keys():
#        print(res[key])
