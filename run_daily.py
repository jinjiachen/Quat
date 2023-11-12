#coding=utf8

#import stock_online
from stock_online import *
import time
from function import is_updated,schedule
from index_online import statistics,live_index
from notification import notify
from jq import auto_check

def daily_combo():
    pro=Initial()
    while True:
        now=time.strftime("%Y%m%d") #当前日期
        if is_updated(pro,'stock',now)=='YES':
            run_daily()
            break

def daily_index():
#    now='20230914'
    pro=Initial()
    while True:
        now=time.strftime("%Y%m%d") #当前日期
        try:
            if is_updated(pro,'index',now)=='YES':
                pass
                print('获取指数信息')
                res=statistics(pro,now,ptf='NO')
                print(res)
                message=f'全市成交量：{res["amount"]}亿,上证涨跌幅：{res["pct_sh"]}% PE:{res["PEttm000001"][0]} 10年百分位：{res["PEttm000001"][1]},PB:{res["PB000001"][0]} 10年百分位：{res["PB000001"][1]},深证涨跌幅：{res["pct_sz"]}% PE:{res["PEttm399001"][0]} 10年百分位：{res["PEttm399001"][1]},'#构造字符串用于推送
                message=[
                        f'全市成交量：{res["amount"]}亿',
                        f'上证涨跌幅：{res["pct_sh"]}%',
                        f'PE:{res["PEttm000001"][0]}-->10年百分位：{res["PEttm000001"][1]},PB:{res["PB000001"][0]}-->10年百分位：{res["PB000001"][1]}',
                        f'深证涨跌幅：{res["pct_sz"]}%',
                        f'PE:{res["PEttm399001"][0]}-->10年百分位：{res["PEttm399001"][1]},PB:{res["PB399001"][0]}-->10年百分位：{res["PB399001"][1]}',
                        ]
                print('构造的消息：',message)
                notify('post',f'日报{now}',"\n".join(message))
                break
        except:
            print('请求出错正在重试！')
            break
#            continue

###获取当前指数信息
def index_now():
    res=live_index()
    message=[f'两市成交量：{res["total_vol"]}亿',
            f'上证：{res["sh"]},上证涨跌幅：{res["sh_pct"]}',
            f'深市：{res["sz"]},深市涨跌幅：{res["sz_pct"]}',
             f'创业板：{res["cyb"]}创业板涨跌幅：{res["cyb_pct"]}',
             f'上证50: {res["sh50"]}, 涨跌幅：{res["sh50_pct"]}',
             f'中证1000: {res["zz1000"]}, 涨跌幅：{res["zz1000_pct"]}',
             f'中证500: {res["zz500"]}涨跌幅：{res["zz500_pct"]}'
            ]
    notify('post','简报',"\n".join(message))


if __name__=='__main__':
#    index_now()
    while True:
        print('当前时间：',time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S")=='15:02:30':
#        if time.strftime("%H:%M:%S")=='16:43:00':
            time.sleep(3)
            print('go!!!')
            index_now()
            daily_combo()
            daily_index()
        if time.strftime("%H:%M:%S")=='06:00:00':
            auto_check()

#    schedule(daily_index,'15:15:00')
#    schedule(daily_combo,'15:15:00')
