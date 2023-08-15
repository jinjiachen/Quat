#coding=utf8

#import stock_online
from stock_online import *
import time
from function import is_updated,schedule


def daily_combo():
    now=time.strftime("%Y%m%d") #当前日期
    pro=Initial()
    while True:
        if is_updated(pro,now)=='YES':
            run_daily()
            break


if __name__=='__main__':
    schedule(daily_combo,'15:15:00')
