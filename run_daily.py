#coding=utf8

#import stock_online
from stock_online import *
import time
from function import is_updated,schedule
from index_online import statistics,live_index
from notification import notify

def daily_combo():
    now=time.strftime("%Y%m%d") #当前日期
    pro=Initial()
    while True:
        if is_updated(pro,'stock',now)=='YES':
            run_daily()
            break

def daily_index():
    now=time.strftime("%Y%m%d") #当前日期
    pro=Initial()
    while True:
        try:
            if is_updated(pro,'index',now)=='YES':
                res=statistics(pro)
                message=f'全市成交量：{res["amount"]}千亿,上证涨跌幅：{res["pct_sh"]}% PE:{pe_sh},深证涨跌幅：{res["pct_sz"]}% PE:{pe_sz}'#构造字符串用于推送
                notify('post',f'日报{now}',message.replace(',','\n'))
                break
        except:
            continue

###获取当前指数信息
def index_now():
    res=live_index()
    message=f'两市成交量：{res["total_vol"]}亿,上证涨跌幅：{res["sh_pct"]},深市涨跌幅：{res["sz_pct"]}'
    notify('post','简报',message.replace(',','\n'))


if __name__=='__main__':
    while True:
        print('当前时间：',time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S")=='15:00:00':
#        if time.strftime("%H:%M:%S")=='16:26:00':
            time.sleep(3)
            print('go!!!')
            index_now()
            daily_combo()
            daily_index()
#    schedule(daily_index,'15:15:00')
#    schedule(daily_combo,'15:15:00')
