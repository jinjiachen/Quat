#coding=utf8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from sqlalchemy import create_engine 
from function import cal_pcts,range_pcts,average_pcts,pcts_list,get_names
from function import get_code_ts 
from xq import get_code as gc_xq
import os,re


def sql_consult(db, date):
    sql="SELECT DISTINCT ts_code,trade_date,close FROM Daily WHERE trade_date="+date; #构建SQL查询语句
    engine_ts = create_engine('mysql://root:administrator@127.0.0.1:3306/'+db+'?charset=utf8&use_unicode=1') ##数据库初始化
    df=pd.read_sql_query(sql, engine_ts) #运用pandas模块read_sql_query方法执行SQL语句
    return df


def pct_chg(period, start, end):
    close_start=sql_consult(db,start)
    close_end=sql_consult(db,end)

def financial_indictor(ts_code,trade_date):
    pro=Initial()
    df=pro.daily_basic(ts_code='', trade_date=trade_date, fields='ts_code,trade_date,pe,pe_ttm,pb,dv_ratio,dv_ttm,turnover_rate')
    df['pe']
    
def summary(file_path,ptf='NO'):#对结果文件总结
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
#    print(res)
    ZB=0#主板
    ZXB=0#中小板
    CYB=0#创业板
    KCB=0#科创板
    BJS=0#北交所
    SZ=0#深证
    SH=0#上证
    bankuai=[]#收集板块信息
    for stock_info in res:
        splice=stock_info.split('\t')
#        print('总长度为',len(splice))
        if ptf=='YES':
            print(len(splice))
            print('正在处理',splice)
            for i,j in enumerate(splice):
                print(str(i)+'-->'+j)
                print(len(j))
        if len(splice)==9 or len(splice)==11:
            bankuai.append(splice[4])
            if splice[6]=='主板':
                ZB+=1
                if 'SZ' in splice[0]:
                    SZ+=1
                elif 'SH' in splice[0]:
                    SH+=1
            elif splice[6]=='创业板':
                CYB+=1
            elif splice[6]=='科创板':
                KCB+=1
            elif splice[6]=='中小板':
                ZXB+=1
        elif len(splice)==8 and '北交所' in stock_info:
            BJS+=1
    
    bankuai_info=pd.value_counts(bankuai)#统计板块次数
    result=f'主板：{ZB}(其中：上证{SH},深圳{SZ}) \n中小板{ZXB} \n创业板：{CYB} \n科创板：{KCB} \n北交所：{BJS} \n总共：{len(res)} \n----------------- \n{bankuai_info}'
#    print(result)
#    print(pd.value_counts(bankuai))
    return result


def daily_push():
    now='20230524'
    df_SH=pro.index_dailybasic(ts_code='000001.SH', trade_date=now, fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')
    pe_SH=df_SH['pe']
    pe_ttm_SH=df_SH['pe_ttm']
    pb_SH=df_SH['pb']

    df_SZ=pro.index_dailybasic(ts_code='390001.SZ', trade_date=now, fields='ts_code,trade_date,turnover_rate,pe,pe_ttm,pb')
    pe_SZ=df_SZ['pe']
    pe_ttm_SZ=df_SZ['pe_ttm']
    pb_SZ=df_SZ['pb']


###计算一段时间内的股票涨跌幅
def stocks_change(start_date,end_date):
    '''
    start_date(str):开始时间，如20240101
    end_date(str):结束时间，如20240101
    '''
    pro=Initial()
    codes_start=pro.daily(trade_date=start_date)
    codes_end=pro.daily(trade_date=end_date)
    codes=pd.merge(codes_start,codes_end,on=['ts_code'],how='inner')
    print(len(codes_start))
    print(len(codes_end))
    print(len(codes))
    print(codes_start)


if __name__=='__main__':
    from stock_online import Initial#防止循环引用模块的错误
    choice=input('1.结果文件分析\n2.一组股票的当日涨跌幅\n3.一组股票一段时间内的涨跌幅\n4.计算一段时间内每一天的平均涨跌幅\n5.计算一组文件的涨跌幅')
    if choice=='1':
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        res=summary(file_path,'YES')
        print(res)
    elif choice=='2':
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        stocklist=gc_xq(file_path)
        names=get_names(stocklist)
        pcts=cal_pcts(stocklist)
        tmp=[]#临时列表，用于拼接股票名称和代码
        for stock,name in zip(stocklist,names):
            tmp.append(stock+ ' '+name)
        for code,pct in zip(tmp,pcts):
            print(code,pct)
        print('综合涨幅：',sum(pcts)/len(pcts))
    elif choice=='3':
        pro=Initial()
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        start=input('请输入开始时间')
        end=input('请输入结束时间')
        stocklist=get_code_ts(file_path)
        names=get_names(stocklist)
        pcts=range_pcts(pro,stocklist,start,end)
        tmp=[]#临时列表，用于拼接股票名称和代码
        for stock,name in zip(stocklist,names):
            tmp.append(stock+ ' '+name)
        for code,pct in zip(tmp,pcts):
            print(code,pct)
        print('组合平均涨跌幅:',sum(pcts)/len(pcts))
    elif choice=='4':
        pro=Initial()
        file_path=input('请输入文件路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
        start=input('请输入开始时间')
        end=input('请输入结束时间')
        stocklist=get_code_ts(file_path)
        pcts=average_pcts(pro,stocklist,start,end)
        print(pcts)
    elif choice=='5':
        path=input('请输入文件夹路径:')
        if os.name=='posix':
            path=path.replace('\' ','')
            path=path.replace('\'','')
        res=pcts_list(path)
        for filename,pct in zip(res[0],res[1]):
            print(filename+'\t\t',pct)
    elif choice=='6':
        stocks_change('20240103','20240607')


