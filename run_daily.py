#coding=utf8

#import stock_online
from stock_online import *
import time
from function import is_updated,schedule
from index_online import statistics
from notification import notify

def daily_combo():
    now=time.strftime("%Y%m%d") #当前日期
    pro=Initial()
    while True:
        if is_updated(pro,now)=='YES':
            run_daily()
            break

def daily_index():
    now=time.strftime("%Y%m%d") #当前日期
    pro=Initial()
    while True:
        if is_updated(pro,now)=='YES':
            res=statistics(pro)
            message=f'全市成交量：{res["amount"]}千亿,上证涨跌幅：{res["pct_sh"]}%,深证涨跌幅：{res["pct_sz"]}%'#构造字符串用于推送
            notify('post',f'日报{now}',message.replace(',','\n'))
            break

if __name__=='__main__':
    while True:
        print('当前时间：',time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S")=='15:15:00':
            time.sleep(3)
            print('go!!!')
            daily_index()
            daily_combo()
#    schedule(daily_index,'15:15:00')
#    schedule(daily_combo,'15:15:00')
