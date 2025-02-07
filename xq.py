import easytrader
import easyquotation
import requests
import random
from lxml import etree
from configparser import ConfigParser
import os,re
import time
import json,base64
from function import cal_pcts




def load_config():#加载配置文件
    conf=ConfigParser()
    if os.name=='nt':
#        path='K:/config.ini'
        path=r'D:\Downloads\PortableGit-2.36.1-64-bit.7z\bin\Quat\config.ini'
    elif os.name=='posix':
        path='/usr/local/src/Quat/config.ini'
    else:
        print('no config file was found!')

    conf.read(path,encoding="utf-8")
    return conf


def Menu():
    combo_li=conf.options('combo')#获取combo这个section下的items,即组合的名称
    for i,combo in enumerate(combo_li):
        print(str(i)+' --> '+combo)
    index=input('请选择对应的组合:')
    index=int(index)
    user=login(login_cookies,conf.get('combo',combo_li[index]))#登录
    choice=input('请选择：\n1.雪球买入\n2.雪球卖出\n3.查询持仓\n4.卖出指定股票')
    if choice=='1':
        quotation=easyquotation.use('sina')
        file_path=input('请输入股票的txt文件')
        if os.name=='posix':
            file_path=file_path.replace('\'','')
            print('revise path:',file_path)
        stock=get_code(file_path)
#        print('获取到的股票代码：',stock)
        buy(stock,user,quotation)
    elif choice=='2':
        adj_weight(user)
    elif choice=='3':
        quotation=easyquotation.use('sina')
        my_pos=position(user,quotation)
        for item in my_pos[0]:
            print(item)
        print('综合涨幅：',my_pos[1])
    elif choice=='4':
        file_path=input('请输入股票的txt文件')
        stock=get_code(file_path)
        for code in stock:
            try:
                sell(user,code,0)
                time.sleep(random.uniform(2,3))
            except:
                print('操作出错')
    elif choice=='da':
        xq_post(login_cookies,'delete',my_stocks(login_cookies))#删除所有雪球自选股
    elif choice=='as':
        file_path=input('输入文件路径或文件夹路径:')
        if os.name=='posix':
            file_path=file_path.replace('\' ','')
            file_path=file_path.replace('\'','')
            print('处理后的文件路径为',file_path)
        if os.path.isfile(file_path):#判断路径是否为文件
            stocklist=get_code(file_path)#获取股票代码
            print('待添加的股票列表',stocklist)
        elif os.path.isdir(file_path):#判断是否为路径
            stocklist=[]
            for root,dirs,files in os.walk(file_path,topdown=False):#遍历路径下的文件和文件夹，返回root,dirs,files的三元元组
                ###读取所有文件中的股票信息并存入stocklist
                for file in files:#遍历所有文件
#                    print(os.path.abspath(file_path+'/'+file))
                    file=os.path.abspath(file_path+'/'+file)#构建文件的绝对路径
                    stocks=get_code(file)#获取文件中的股票信息
                    ###存储股票信息
                    for stock in stocks:
                        stocklist.append(stock)
#                print(stocklist)
        xq_post(login_cookies,'add',stocklist)#增加雪球自选股




def login(login_cookies,combo):#雪球的登录
    '''
    login_cookies:雪球的cookies
    combo:组合的名称
    '''
    user=easytrader.use('xq')#使用雪球
    user.prepare(
        cookies=login_cookies,
        portfolio_code=combo,
        portfolio_market='cn'
        )
    #print(user.position)
    #print(user.balance)
    return user


def get_code(file_path):#提取致富代码
    '''
    file_path(str):提取文件的路径
    '''
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
        stock_code=[] #构造空列表，用来存储股票代码

        #通过判断第一行的数据来确定数据来源
        firstline=res[0]#获取第一行来判断数据来源
        if re.search('\d{6}.XSH[GE]',firstline)!=None:
            source='jq'
        elif re.search('\d{6}.S[HZ]',firstline)!=None:
            source='ts'

        #根据不同的数据来源进行处理
        if source=='ts':
            for i in res:#遍历所有的结果
                if '\t' in i:
                    stock_code.append(i.split('\t')[0].split('.')[1]+i.split('\t')[0].split('.')[0])#提取结果中的致富代码并作简单处理，如'sz000001'
                else:
                    i=i.replace('\n','')#去除换行符
                    i=i.split('.')[1]+i.split('.')[0]#转化成雪球的格式
                    stock_code.append(i)
        elif source=='jq':
            for i in res:#遍历所有的结果
                code_jq=re.search('\d{6}.XSH[GE]',i).group()#用正则提取股票代码
                if 'XSHE' in code_jq:
                    code_xq='SZ'+code_jq[:6]#转换成雪球代码
                elif 'XSHG' in code_jq:
                    code_xq='SH'+code_jq[:6]#转换成雪球代码
                stock_code.append(code_xq)
    return stock_code 


def buy(stock_list,user,quotation):
    splice=int(100/len(stock_list))
    current=user.balance[0]['current_balance']#现金余额
    current_splice=int(current/len(stock_list))#按照股票数量等分
    for stock_code in stock_list:
        while True:
            try:
                stock_code=stock_code.lower()
                price_now=quotation.real(stock_code)[stock_code[2:]]['now']
                if price_now==0:
                    pass
                else:
                    amount=int((current_splice/price_now))
                user.buy(stock_code,price=price_now,amount=amount)
                time.sleep(random.randint(1,3))
                break
            except:
                print('太过于频繁，等待后重试！')
                time.sleep(5)
                
def sell(user,stock_code,amount):#卖出指定股票
    flag=1#返回码，执行成功为0，不成功为1，默认为1

    #判断股票是否在持仓中
    my_pos=user.position
#    for position in user.position:
    for position in my_pos:
        print('正在比对',position['stock_code'])
        if stock_code in position['stock_code']:
            print(f'找到持仓股票{stock_code},进行卖出操作！')
            try:
                #如果股票在持仓中，则进行卖出操作
                user.adjust_weight(stock_code,amount)
                flag=0#卖出成功，返回0
                time.sleep(random.randint(1,3))
            except:
                print('正在重新尝试！')
    if flag==1:
        print(f'股票{stock_code}不在持仓中，不能进行卖出操作!')
    return flag

def adj_weight(user):
#    pos=user.position#delete later
    for position in user.position:
        try:
            stock_code=position['stock_code'][2:]#提取股票代码的数字部分
            if len(user.position)>1:
                user.adjust_weight(stock_code,0)
            else:
                user.adjust_weight(stock_code,1)
        except:
            print('太过于频繁，等待后重试！')
            time.sleep(5)

def position(user,quotation):#get position for specific combo
#    pos=user.position#delete later
#    print(pos)
    stock_name=[]
    stock_code=[]
    pct=[]
    my_pos=[]
    for position in user.position:
        stock_code.append(position['stock_code'])#提取股票代码
        stock_name.append(position['stock_name'])#name

    #获取持仓股票对应的涨跌幅
    for stock in stock_code:#遍历股票列表
        stock=stock[2:]#去除开头SH,SZ，保留数字部分
        stock_info=quotation.real(stock)#查询股票的价格信息
        close=stock_info[stock]['close']#昨日收盘价
        now=stock_info[stock]['now']#当前价格
        cal_pct=round((now/close-1)*100,2)#计算涨跌幅
        pct.append(str(cal_pct))

    #获取持仓的综合收益
    pcts=cal_pcts(stock_code)#计算一组股票的涨跌幅
    pcts_overall=sum(pcts)/len(pcts)

    #结果的收集
    for index in range(0,len(stock_code)):
        my_pos.append(str(index+1)+'. '+stock_code[index]+'\t'+stock_name[index]+'\t'+pct[index])
    return [my_pos,pcts_overall]#返回一个列表，分别为每个股票涨跌幅和综合涨幅

def xq_post(login_cookies,method,stocklist):#模拟雪球的请求
    '''
    login_cookies(str):雪球的cookie
    method(str):delete,add
    stocklist(list):股票的列表
    '''
    header={
                'Accept':'application/json, text/plain, */*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    #            'Content_Type':'application/x-www-form-urlencoded',
                'Cookie':login_cookies,
                'Origin':'https://xueqiu.com',
                'Refer':'https://xueqiu.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1474.0'
                }
    if method=='delete':#删除所有自选股票
        url='https://stock.xueqiu.com/v5/stock/portfolio/stock/cancel.json'
    elif method=='add': #加入自选
        url='https://stock.xueqiu.com/v5/stock/portfolio/stock/add.json'
    for stock in stocklist:
        data={
            'symbols':stock,
            }
        print(f'正在{method}股票:',stock)
        res=requests.post(url,headers=header,data=data)


#    while True:
#            res=requests.post(url,headers=header,data=data)
#            print(res.text)
#        try:
    #    res=requests.get(url,headers=header,params=data,verify=False)#方法1
#            res=requests.post(url,headers=header,data=data)
#            print(res.text)
#            html=res.text
#            selector=etree.HTML(html)#转化为lxml
#            return selector
#            break
#        except:
#            print('连接超时，正在重新连接！')


def my_stocks(login_cookies):#获取自选股票的持仓
    '''
    login_cookies(str):雪球的cookie
    '''
    url='https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=1&pid=-1'
    header={
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie':login_cookies,
            'Origin':'https://xueqiu.com',
            'Refer':'https://xueqiu.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1474.0',
            }

    res=requests.get(url,headers=header,timeout=5,verify=False)#get方法,返回json格式的字符串
    res_json=json.loads(res.text)#加载字符串的json数据
    content=res_json['data']['stocks']#获取股票信息列表
    stocklist=[]
    for code in content:
        stocklist.append(code['symbol'])
#    print(res.text)
    return stocklist 



if __name__=='__main__':
    conf=load_config()
    login_cookies=conf.get('cookies','xq')
    login_cookies=base64.b64decode(login_cookies).decode('ascii')#base64解码后的cookie
    while True:
        Menu()
        input('press ANY THING to contine!')
        if os.name=='nt':
            os.system('cls')
        elif os.name=='posix':
            os.system('clear')
