import easytrader
import easyquotation
from configparser import ConfigParser
import os

def read_config(section,item):
    conf=ConfigParser()
    path='/usr/local/src/Quat/config.ini'
    conf.read(path,encoding="utf-8")
    return conf.get(section,item)

def Menu():
    choice=input('请选择：\n1.雪球买入\n2.雪球卖出')
    if choice=='1':
        user=login()
        quotation=easyquotation.use('sina')
        file_path=input('请输入股票的txt文件')
        stock=get_code(file_path)
        buy(stock,user,quotation)
    elif choice=='2':
        user=login()
        adj_weight(user)


def login():#雪球的登录
    user=easytrader.use('xq')#使用雪球
    login_cookie=read_config('cookies','xq')
    user.prepare(
        cookies=login_cookie,
        portfolio_code='ZH3162090',
        portfolio_market='cn'
        )
    #print(user.position)
    #print(user.balance)
    return user


def get_code(file_path):#提取致富代码
#    file_path='/usr/local/src/tushare/result/Mbottom13_12_1_20220903loc.txt'#筛选出来的结果文件
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()
        stock_code=[] #构造空列表，用来存储股票代码
        for i in res:#遍历所有的结果
            stock_code.append(i.split('\t')[0].split('.')[1]+i.split('\t')[0].split('.')[0])#提取结果中的致富代码并作简单处理，如'sz000001'
    return stock_code 


def buy(stock_list,user,quotation):
    splice=int(100/len(stock_list))
    current=user.balance[0]['current_balance']#现金余额
    current_splice=int(current/len(stock_list))#按照股票数量等分
    for stock_code in stock_list:
        stock_code=stock_code.lower()
        price_now=quotation.real(stock_code)[stock_code[2:]]['now']
        if price_now==0:
            pass
        else:
            amount=int((current_splice/price_now))
        user.buy(stock_code,price=price_now,amount=amount)

def adj_weight(user):
    pos=user.position
    for position in user.position:
        stock_code=position['stock_code'][2:]#提取股票代码的数字部分
        if len(user.position)>1:
            user.adjust_weight(stock_code,0)
        else:
            user.adjust_weight(stock_code,1)


if __name__=='__main__':
    Menu()
