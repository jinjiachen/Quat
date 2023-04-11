import easytrader
import easyquotation
from configparser import ConfigParser
import os
import time



def load_config():#加载配置文件
    conf=ConfigParser()
    if os.name=='nt':
        path='K:/config.ini'
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
        for item in my_pos:
            print(item)
    elif choice=='4':
        file_path=input('请输入股票的txt文件')
        stock=get_code(file_path)
        for code in stock:
            try:
                sell(user,code,0)
                time.sleep(random.uniform(2,3))
            except:
                print('操作出错')



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
        while True:
            try:
                stock_code=stock_code.lower()
                price_now=quotation.real(stock_code)[stock_code[2:]]['now']
                if price_now==0:
                    pass
                else:
                    amount=int((current_splice/price_now))
                user.buy(stock_code,price=price_now,amount=amount)
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

            #如果股票在持仓中，则进行卖出操作
            user.adjust_weight(stock_code,amount)
            flag=0#卖出成功，返回0
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

    #结果的收集
    for index in range(0,len(stock_code)):
        my_pos.append(str(index+1)+'. '+stock_code[index]+'\t'+stock_name[index]+'\t'+pct[index])
    return my_pos


if __name__=='__main__':
    conf=load_config()
    login_cookies=conf.get('cookies','xq')
    while True:
        Menu()
        input('press ANY THING to contine!')
        if os.name=='nt':
            os.system('cls')
        elif os.name=='posix':
            os.system('clear')
