#coding=utf8

#import stock_online
from stock_online import *
import time,os,base64,sys
from datetime import datetime
from function import is_updated,schedule
from index_online import statistics,live_index
from notification import notify
from jq import auto_check
from xq import my_stocks,xq_post,load_config,get_code

def daily_combo():
    pro=Initial()
    while True:
        now=time.strftime("%Y%m%d") #当前日期
        df=pro.trade_cal(start_date=now,end_date=now)
        if is_updated(pro,'stock',now)=='YES':#交易日
#        if df['is_open'][0]==1:#交易日
            run_daily()
            break
#        elif is_updated(pro,'stock',now)=='NO':#非交易日
        elif df['is_open'][0]==0:#非交易日
            break

def daily_index():
#    now='20230914'
    pro=Initial()
    while True:
        now=time.strftime("%Y%m%d") #当前日期
        df=pro.trade_cal(start_date=now,end_date=now)
        try:
#            if is_updated(pro,'index',now)=='YES':#交易日
            if df['is_open'][0]==1:#交易日
                print('获取指数信息')
                res=statistics(pro,now,ptf='NO')
                print(res)
#                message=f'全市成交量：{res["amount"]}亿,上证涨跌幅：{res["pct_sh"]}% PE:{res["PEttm000001"][0]} 10年百分位：{res["PEttm000001"][1]},PB:{res["PB000001"][0]} 10年百分位：{res["PB000001"][1]},深证涨跌幅：{res["pct_sz"]}% PE:{res["PEttm399001"][0]} 10年百分位：{res["PEttm399001"][1]},'#构造字符串用于推送
                message=[
                        f'全市成交量：{res["amount"]}亿',
                        f'全市总市值：{res["total_mv"]}万亿',
#                        f'全市总市值：{res["total_mv"]}万亿--> {res["total_mv_pct"]}',
                        f'上证涨跌幅：{res["close_sh"]}-->{res["pct_sh"]}%-->PP 10年百分位{res["PP000001"]}',
                        f'PE:{res["PEttm000001"][0]}-->10年百分位：{res["PEttm000001"][1]}\nPB:{res["PB000001"][0]}-->10年百分位：{res["PB000001"][1]}',
                        '#'*25,
                        f'深证涨跌幅：{res["close_sz"]}-->{res["pct_sz"]}-->PP 10年百分位{res["PP399001"]}%',
                        f'PE:{res["PEttm399001"][0]}-->10年百分位：{res["PEttm399001"][1]}\nPB:{res["PB399001"][0]}-->10年百分位：{res["PB399001"][1]}',
                        '#'*25,
                        f'沪深300涨跌幅：{res["close_hs300"]}-->{res["pct_hs300"]}-->PP 10年百分位{res["PP000300"]}%',
                        f'PE:{res["PEttm000300"][0]}-->10年百分位：{res["PEttm000300"][1]}\nPB:{res["PB000300"][0]}-->10年百分位：{res["PB000300"][1]}',
                        '#'*25,
                        f'中证500涨跌幅：{res["close_zz500"]}-->{res["pct_zz500"]}-->PP 10年百分位{res["PP000905"]}%',
                        f'PE:{res["PEttm000905"][0]}-->10年百分位：{res["PEttm000905"][1]}\nPB:{res["PB000905"][0]}-->10年百分位：{res["PB000905"][1]}',
                        '#'*25,
                        f'上证50涨跌幅：{res["close_sz50"]}-->{res["pct_sz50"]}-->PP 10年百分位{res["PP000016"]}%',
                        f'PE:{res["PEttm000016"][0]}-->10年百分位：{res["PEttm000016"][1]}\nPB:{res["PB000016"][0]}-->10年百分位：{res["PB000016"][1]}',
                        '#'*25,
                        f'创业板涨跌幅：{res["close_cyb"]}-->{res["pct_cyb"]}-->PP 10年百分位{res["PP399006"]}%',
                        f'PE:{res["PEttm399006"][0]}-->10年百分位：{res["PEttm399006"][1]}\nPB:{res["PB399006"][0]}-->10年百分位：{res["PB399006"][1]}',
                        ]
                print('构造的消息：',message)
                notify('post',f'日报{now}',"\n".join(message))
                break
#            elif is_updated(pro,'index',now)=='NO':#非交易日
            elif df['is_open'][0]==0:#非交易日
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
            f'沪深300：{res["hs300"]},深市涨跌幅：{res["hs300_pct"]}',
             f'创业板：{res["cyb"]}创业板涨跌幅：{res["cyb_pct"]}',
             f'上证50: {res["sh50"]}, 涨跌幅：{res["sh50_pct"]}',
             f'中证500: {res["zz500"]}涨跌幅：{res["zz500_pct"]}',
             f'中证1000: {res["zz1000"]}, 涨跌幅：{res["zz1000_pct"]}',
             f'国证2000: {res["gz2000"]}, 涨跌幅：{res["gz2000_pct"]}',
            ]
    notify('post','简报',"\n".join(message))

###自动同步当天的股票结果到雪球自选
def xq_sync(login_cookies):
    try:
        xq_post(login_cookies,'delete',my_stocks(login_cookies))#删除所有雪球自选股
        stocklist=[]
        today=datetime.now().strftime('%Y%m%d')
        file_path='/usr/local/src/Quat/result/'+today
        for root,dirs,files in os.walk(file_path,topdown=False):#遍历路径下的文件和文件夹，返回root,dirs,files的三元元组
            ###读取所有文件中的股票信息并存入stocklist
            for file in files:#遍历所有文件
                print(os.path.abspath(file_path+'/'+file))
                file=os.path.abspath(file_path+'/'+file)#构建文件的绝对路径
                stocks=get_code(file)#获取文件中的股票信息
                ###存储股票信息
                for stock in stocks:
                    stocklist.append(stock)
        xq_post(login_cookies,'add',stocklist)#增加雪球自选股
        notify('post','同步持仓','已完成同步')
    except:
        notify('post','同步持仓','同步失败，可能是cookie过期')

if __name__=='__main__':
    conf=load_config()
    login_cookies=conf.get('cookies','xq')
    login_cookies=base64.b64decode(login_cookies).decode('ascii')#base64解码后的cookie
    if len(sys.argv)=="1":
        while True:
            print('当前时间：',time.strftime("%H:%M:%S"))
            if time.strftime("%H:%M:%S")=='15:00:30':
                time.sleep(3)
                print('go!!!')
                index_now()
            if time.strftime("%H:%M:%S")=='16:00:00':
                daily_combo()
                daily_index()
                xq_sync(login_cookies)#同步当天结果到雪球自选
            if time.strftime("%H:%M:%S")=='06:00:00':
                if os.name=='nt':
                    auto_check()
    elif sys.argv[1]=="index":
        index_now()
    elif sys.argv[1]=="index_ts":
        daily_index()
    elif sys.argv[1]=="combo":
        daily_combo()
        xq_sync(login_cookies)#同步当天结果到雪球自选
    elif sys.argv[1]=="sync":
        xq_sync(login_cookies)#同步当天结果到雪球自选

#    schedule(daily_index,'15:15:00')
#    schedule(daily_combo,'15:15:00')
