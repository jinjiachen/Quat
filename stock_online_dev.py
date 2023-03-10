#coding=utf8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue
from xq import load_config

def Initial():#初始化
    conf=load_config()
    my_token=conf.get('tushare','account2')
    ts.set_token(my_token)
    pro=ts.pro_api()
    return pro

def Stocklist():#获取股票列表
    sl=pro.stock_basic(exchange='',list_status='L',fields='ts_code')
    return sl
#    print(sl) #调试用

def Wait(n):
    i=0
    while i<n:
        i+=1

def Menu():
    print("请选择选股模型:")
    print("1.均线金叉模型")
    print("2.均线压制K线多时,K线站上均线模型")
    print("3.均线拐头模型")
    print("4.趋势模型")
    print("all:以上所有模型")
    choice=input()
    if choice=="1":
        freq=input("请输入均线周期:")
        mas=input("请输入短期均线:")
        mal=input("请输入长期均线:")
        n=input("请输入跨越的周期长度:")
        m=input("几天内金叉:")
        result=GoldenCross(freq,int(mas),int(mal),int(n),int(m))
        filename=freq+'cross'+mas+mal+'_'+n+'_'+m+'_'+now+'.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=="2":
        freq=input("请输入均线周期:")
        mas=input("请输入均线:")
        n=input("请输入跨越的周期长度:")
        m=input("K线在多长时间内站上均线:")
        result=Suppress(freq,int(mas),int(n),int(m))
        filename=freq+'suppress'+mas+'_'+n+"_"+m+'_'+now+'.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='3':
        freq=input("请输入均线周期:")
        ma_s=input("请输入均线:")
        n=input("请输入跨越的周期长度:")
        m=input("均线拐头天数:")
        result=Bottom(freq,int(ma_s),int(n),int(m))
        filename=freq+'bottom'+ma_s+'_'+n+"_"+m+'_'+now+'.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='4':
        freq=input("请输入均线周期:")
        ma_s=input("请输入均线:")
        n=input("请输入跨越的周期长度:")
        m=input("均线趋势上扬时间:")
        result=Suppress(freq,int(ma_s),int(n),int(m))
        filename=freq+'trend'+ma_s+'_'+n+"_"+m+'_'+now+'.txt' #文件名
        SaveResult(filename,result) #保存结果
    elif choice=='all':
        print("正在设定均线金叉模型参数:")
        freq1=input("请输入均线周期:")
        mas=input("请输入短期均线:")
        mal=input("请输入长期均线:")
        n1=input("请输入跨越的周期长度:")
        result=Cross(freq1,int(mas),int(mal),int(n1))
        print("正在设定均均线压制K线多时,K线站上均线模型参数:")
        freq2=input("请输入均线周期:")
        n2=input("请输入跨越的周期长度:")
        result=Suppress(freq2,int(n2))

def SaveResult(filename,result):        
#    with open ('/usr/local/src/tushare/result/'+filename,'w') as f:
    with open ('/usr/local/src/Quat/result/'+filename,'w') as f:
        for i in result:
            details=StockDetails(i)
            Wait(50000)
            for j in details:
                f.write(j)
            f.write('\n') 
        f.close()

def StockDetails(ts_code):
    details=[] #记录股票详细信息
    tmp=pro.stock_basic(ts_code=ts_code) #获取DataFrame结构的信息
    for i in tmp.loc[0]: #遍历DataFrame中的label:0
        if i!=None:
            details.append(i+'\t')
    return details



def Cross(freq,mas,mal,n): #均线交叉
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=ts.pro_bar(ts_code=i,freq=freq,adj='qfq',start_date=previous,end_date=now,ma=[mas,mal])
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma_s=data['ma'+str(mas)] #提取短期均线
        ma_l=data['ma'+str(mal)] #提取长期均线
        if len(ma_s)<n or len(ma_l)<n: #判断是否有空值
#            print(i+'上市时间过短')
            continue
        if (ma_s[0]-ma_l[0])>0 and (ma_s[n]-ma_l[n])<0:
            result.append(i)
#            print('捕获:'+data['ts_code'])
        if freq=='W':
            Wait(15000) #等待一段时长，防止频率过快，受限于帐号积分
        if freq=='M':
            Wait(5000000) #等待一段时长，防止频率过快，受限于帐号积分
#    print(ma13)
#    plt.plot(data['trade_date'],data['ma13'])
#    plt.plot(data['trade_date'],data['ma55'])
#    plt.show()
    return result

def GoldenCross(freq,mas,mal,n,m): #均线金叉
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=ts.pro_bar(ts_code=i,freq=freq,adj='qfq',start_date=previous,end_date=now,ma=[mas,mal])
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma_s=data['ma'+str(mas)] #提取短期均线
        ma_l=data['ma'+str(mal)] #提取长期均线
        if len(ma_s)<n or len(ma_l)<n: #判断是否有空值
            continue
        if ma_s[0]>ma_l[0]: #判断短期均线是不是在长期均线上方
            j=1
            crosspoint=0 #初始值为0,假设1天内出现金叉的情况
            while j<=n: #判断之前的收盘价是不是在均线下文，以此寻找刚启动的行情
                if ma_s[j]>ma_l[j]: #判断短期均线是否还在长期均线上方，不是则交叉点已经出现
                    crosspoint=j #记录金叉时的天数
                    j=j+1
                else:
                    if crosspoint<=m: #判断交叉点是否在要求的时间段里,是则继续判断
                        j+=1
                        if j==n: #交叉前的N天，短期均线都在长期均线下方,可以断定为金叉
                            result.append(i)
                    else:
                        break
        if freq=='W':
            Wait(20000) #等待一段时长，防止频率过快，受限于帐号积分
        if freq=='M':
            Wait(9000000) #等待一段时长，防止频率过快，受限于帐号积分
    return result

def Suppress(freq,mas,n,m): #K线站上均线模型
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('Suppress进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=ts.pro_bar(ts_code=i,freq=freq,adj='qfq',start_date=previous,end_date=now,ma=[mas])
#        data1=ts.pro_bar(ts_code=i,freq='D',adj='qfq',start_date=previous,end_date=now,ma=[mas])
#        data.to_csv('/tmp/online.csv')
#        break
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        Wait(20000000) #等待一段时长，防止频率过快，受限于帐号积分
        close=data['close']
        ma=data['ma'+str(mas)]
        if len(close)<n or len(ma)<n: #判断是否有空值
            continue
        if close[0]>ma[0]: #判断最新收盘价是不是在均线上方
            j=1
            point=0
            while j<=n: #判断之前的收盘价是不是在均线下文，以此寻找刚启动的行情
                if close[j]>ma[j]: #判断K线是否还在长期均线上方，不是则突破压制
                    point=j #记录突破时的天数
                    j=j+1
                else:
                    if point==m: #判断突破是否在要求的时间段里,是则继续判断
                        if j==n: #突破前的N段时间内，都在均线下方，突破成立
                            result.append(i)
                        j+=1
                    else:
                        break
    return result

def Trend(freq,ma_s,n): #单调递增模型
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=ts.pro_bar(ts_code=i,freq=freq,adj='qfq',start_date=previous,end_date=now,ma=[ma_s])
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma=data['ma'+str(ma_s)]
        if len(ma)<n: #判断是否有空值
            continue
        j=0 #循环初始化
        while ma[j]>ma[j+1]:
            if j==n: #n天内，均线单调递增
                result.append(i)
                break
            j+=1
        if freq=='W':
            Wait(5000000) #等待一段时长，防止频率过快，受限于帐号积分
        if freq=='M':
            Wait(5000000) #等待一段时长，防止频率过快，受限于帐号积分
    return result
                

def Bottom(sl,freq,ma_s,n,m): #均线拐点
    count=0 #计数
    total=len(sl['ts_code']) #总上市股票数
    result=[]
    for i in sl['ts_code']:
        os.system('clear')
        count+=1 #每判断一个股票，计数加1
        print('Bottom进度:'+str(count)+'/'+str(total)) #显示已判断股票数的比例
        print('正在比对:'+i) #调试用
        data=ts.pro_bar(ts_code=i,freq=freq,adj='qfq',start_date=previous,end_date=now,ma=[ma_s])
        if data is None: #如果没有获取到任何数据，比如刚上市又还没上市的股票
            continue
        ma=data['ma'+str(ma_s)] #提取均线
        close=data['close'] #提取收盘价
        if len(ma)<n: #判断是否有空值
            continue
        if close[0]<ma[0]: #收盘价在均线上方，如在均线下文，则为弱势
            continue
        j=0 #初始化
        if ma[j]>ma[j+1]: #判断当前均值是否大于前一天，即均线拐头,如不是，则均线向下，不合要求，排除
            j=j+1
            while ma[j]>ma[j+1]: #向前递归，直到出现拐点
                j=j+1
            point=j #记录拐点
        else:
            continue
        if point==m: #拐点是否在要求的时间
            while ma[j]<=ma[j+1]: #向前递归，拐点前是否单调递减
                j=j+1
                if j==n: #直到规定的时间内，都是单调递减，则输出
                    result.append(i)
                    break #捕捉到致富代码，则退出循环，寻找下一个

        if freq=='D':
            Wait(5000000) #等待一段时长，防止频率过快，受限于帐号积分
        if freq=='W':
            Wait(500000) #等待一段时长，防止频率过快，受限于帐号积分
        if freq=='M':
            Wait(950000000) #等待一段时长，防止频率过快，受限于帐号积分
    q.put(result)
    return result



####主程序####
if __name__ == '__main__':
    pro=Initial() #初始化
    q=Queue()
    now=time.strftime("%Y%m%d") #当前日期
    #now='20201230'
    previous=int(now)-30000 #一年前的日期
    previous=str(previous) #转换成字符串
    sl=Stocklist() #股票列表
#    sl=sl[1:20] #调试用，限制股票数量以减短时间
#    global result
#    result=[]#全局变量，记录结果
    start=time.time()
#    t1=Thread(target=Bottom,args=(sl[100:200],'D',13,15,1))
#    t2=Thread(target=Suppress,args=('D',13,15,1))
#    t1.start()
#    t2.start()
#    t1.join()
#    t2.join()

    t1=Process(target=Bottom,args=(sl[100:200],'D',13,15,1))
#    t2=Process(target=Bottom,args=(sl[500:999],'D',13,15,1))
#    t3=Process(target=Bottom,args=(sl[1000:1499],'D',13,15,1))
#    t4=Process(target=Bottom,args=(sl[1500:1999],'D',13,15,1))
#    t5=Process(target=Bottom,args=(sl[2000:2499],'D',13,15,1))
#    t6=Process(target=Bottom,args=(sl[2500:2999],'D',13,15,1))
#    t7=Process(target=Bottom,args=(sl[3000:3499],'D',13,15,1))
#    t8=Process(target=Bottom,args=(sl[3500:3999],'D',13,15,1))
#    t9=Process(target=Bottom,args=(sl[4000:4499],'D',13,15,1))
#    t10=Process(target=Bottom,args=(sl[4500:4999],'D',13,15,1))
    t1.start()
#    t2.start()
#    t3.start()
#    t4.start()
#    t5.start()
#    t6.start()
#    t7.start()
#    t8.start()
#    t9.start()
#    t10.start()
    t1.join()
#    t2.join()
#    t3.join()
#    t4.join()
#    t5.join()
#    t6.join()
#    t7.join()
#    t8.join()
#    t9.join()
#    t10.join()
#    Bottom('D',13,15,1)
#    Suppress('D',13,15,1)
    end=time.time()
    result=q.get()
    print(end-start)
    print(result)



#    Menu()
    #result=Cross('W',13,55,2) #调试用
    #result=Suppress('M',8,10) #调试用
    #result=GoldenCross('D',8,21,3,1) #调试用
    #result=Trend('W',55,50) #调试用
    #result=Bottom('D',55,10,2) #调试用
    #SaveResult('test',result) #调试用

