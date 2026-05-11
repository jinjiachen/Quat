import json,os,base64,time,random,re
import uuid
import hashlib
import base64
import requests
from configparser import ConfigParser

def load_config():#加载配置文件
    conf=ConfigParser()
    if os.name=='nt':
#        path=r'.\config.ini'
        path=r'D:\Downloads\PortableGit-2.36.1-64-bit.7z\bin\Quat\config.ini'
    elif os.name=='posix':
        path='/usr/local/src/Quat/config.ini'
    else:
        print('no config file was found!')

    conf.read(path,encoding="utf-8")
    return conf

# ===================== 【固定配置：已帮你填好】 =====================
conf=load_config()#读取配置文件
key=conf.get('gszq','key')
CONFIG = {
    "signKey": key,
    "merchant_id": "trade",
    "encryMode": ""  # 无加密，用 base64
}
# ==================================================================

# ===================== 【必填：你自己的Cookie】 =====================
# 把你抓包的完整Cookie粘贴这里
COOKIE_STR = conf.get("gszq","cookie")
COOKIE_STR=base64.b64decode(COOKIE_STR).decode('ascii')#base64解码
account=conf.get("gszq","account")
account=base64.b64decode(account).decode('ascii')#base64解码
phone=conf.get("gszq","phone")
phone=base64.b64decode(phone).decode('ascii')#base64解码
password=conf.get("gszq","password")
wid=conf.get("gszq","wid")
stock_A=conf.get("gszq","stock_A")#沪市账户
stock_S=conf.get("gszq","stock_S")#深市账户
# ==================================================================

# ===================== 请求头（固定不变） =====================
HEADERS = {
    "Host": "h5jy.gszq.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Linux; Android 16; PLJ110 Build/BP2A.2506015; wv) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://h5jy.gszq.com/m/trade/views/stock/stockQueryToday.html",
    "Cookie": COOKIE_STR.strip()
}
# ==============================================================


# ===================== 公用参数 =====================
url = "https://h5jy.gszq.com/servlet/call"

# 业务参数（填你的资金账号）
PARAM = {
"entrust_way": "6",
"branch_no": "301",
"fund_account": account,  # 替换成你的资金账号
"cust_code": account,     # 替换成你的客户代码
"password": password,
"session_id": "",
"money_type": "",
"flag": "0",
"wid": wid,
"sysnode_id": "2",
"op_station": f"2| | | | |{phone}| |wechat|2.0.1| | | | | |Android| | | ",
"_t":str(int(time.time()))
#    "stock_code": "600000",         # 股票代码（查询可随便填）
#    "exchange_type": "1"            # 1=沪市 2=深市
}


# ------------------------- 工具函数（内置库，无报错） -------------------------
# base64编码（对应网页JS逻辑）
def base64_encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

# MD5加密+大写（网页签名规则）
def md5_upper(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest().upper()

# ------------------------- 核心：生成合法 post_data（1:1复刻JS） -------------------------
def build_post_data(bizcode, param):
    # 1. 业务参数转json + base64编码（你的环境无aes/des加密）
    #json_param = json.dumps(param, ensure_ascii=False)
    json_param = json.dumps(param, ensure_ascii=False, separators=(',', ':'), sort_keys=False)
    data = base64_encode(json_param)
   
    # 2. 公共参数
    request_id = str(uuid.uuid4())
    service_param = {
        "bizcode": bizcode,
        "data": data,
        "merchant_id": CONFIG["merchant_id"],
        "request_id": request_id,
        "signKey": CONFIG["signKey"]
    }

    # 3. 固定顺序拼接（和网页JS完全一致）
    arr = ["bizcode", "data", "merchant_id", "request_id", "signKey"]
    sign_str = "&".join([f"{k}={service_param[k]}" for k in arr])

    # 4. 生成签名
    sign = md5_upper(sign_str)

    # 5. 生成最终post data（去掉signKey，加上sign）
    final_str = "&".join([f"{k}={service_param[k]}" for k in arr[:-1]]) + f"&sign={sign}"
    
    return final_str


###获取文件信息
def get_data(file_path,ptf='NO'):
    '''
    file_path(str):jq持仓信息的文件路径
    '''
    #读取文件内容
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()

    #提取文件中的股票和数量信息
    codes_jq=[]
    nums_jq=[]
    for line in res:
        code_jq=re.search(r'\d{6}.XSH[GE]',line).group()#用正则提取股票代码
        num_jq=re.search(r'-?\d+股',line).group()
        num_jq=num_jq.replace('股','')
        if 'XSHE' in code_jq:
            code_jq=code_jq[:6]+'.SZ'#转换成tushare,hb代码
        elif 'XSHG' in code_jq:
            code_jq=code_jq[:6]+'.SH'#转换成tushare,hb代码
        codes_jq.append(code_jq)
        nums_jq.append(num_jq)
        if ptf=='YES':
            print(f'从文件中提取的股票:{code_jq},对应的数量:{num_jq}')
    return [codes_jq,nums_jq]


###构建买卖的股票基本信息并下单
def order(act,stock_code,price,amount):
    '''
    act(str):买卖
    code(str):代码
    price(float):价格
    amount(int):数量
    '''
    if act=='buy':
        entrust_bs="0"
        BIZCODE = "301501"
    elif act=='sell':
        entrust_bs="1"
        BIZCODE = "301502"
    if 'sz' in stock_code.lower():
        stock_account=stock_S
        exchange_type="0"
    elif 'sh' in stock_code.lower():
        stock_account=stock_A
        exchange_type="2"
    ORDER_PARAM = {
    "entrust_way": "6",
    "branch_no": "301",
    "fund_account": account,  # 替换成你的资金账号
    "cust_code": account,     # 替换成你的客户代码
    "password": password,
    "session_id": "",
    "entrust_bs":entrust_bs,#买卖不同，好像买是0,卖是1
    "exchange_type":exchange_type,            # 2=沪市 0=深市
    "stock_account":stock_account,#沪市深市帐号不同
    "stock_code":stock_code,#大小写不敏感
    "entrust_price":price,
    "entrust_amount":amount,
    "userID":"DID",
    "business_version":"2",
    "wid": wid,
    "sysnode_id": "2",
    "op_station": f"2| | | | |{phone}| |wechat|2.0.1| | | | | |Android| | | ",
    "_t":str(int(time.time()))
    }
    post_data = build_post_data(BIZCODE, ORDER_PARAM)
    response = requests.post(url, headers=HEADERS, data=post_data)
    return response



###根据get_data获取的信息进行批量的买卖
def orders(act,lists):
    pass


###同步jq组合的持仓
def sync_jq(file_path,ptf='NO'):
    '''
    file_path(str):jq持仓信息的文件路径
    '''
    #读取文件内容
    with open(file_path,'r') as f:
        res=f.readlines()#按行读取文件中的内容，每一行为一个字符串，返回以字符串为元素的列表
        f.close()

    #提取文件中的股票和数量信息
    codes_jq=[]
    nums_jq=[]
    for line in res:
        code_jq=re.search(r'\d{6}.XSH[GE]',line).group()#用正则提取股票代码
        num_jq=re.search(r'-?\d+股',line).group()
        num_jq=num_jq.replace('股','')
        if 'XSHE' in code_jq:
            code_jq=code_jq[:6]+'.SZ'#转换成tushare,hb代码
        elif 'XSHG' in code_jq:
            code_jq=code_jq[:6]+'.SH'#转换成tushare,hb代码
        codes_jq.append(code_jq)
        nums_jq.append(num_jq)
        if ptf=='YES':
            print(f'从文件中提取的股票:{code_jq},对应的数量:{num_jq}')

    #获取持仓信息，和文件内容进行比对
    positions=get_position()#获取持仓
    final_num=[]
    for code,num in zip(codes_jq,nums_jq):
        amount=None#数量初始化为空
        for pos in positions:
            if code==pos[1]:#比较股票代码，判断是否有持仓pos[1]为股票代码
                #amount=int(num)-int(pos[6])#如果有持仓,比较jq和hb的数量差pos[6]为可卖股票数量,pos[5]为持有数量
                amount=int(num)-int(pos[5])#如果有持仓,比较jq和hb的数量差pos[6]为可卖股票数量,pos[5]为持有数量
                break
        if amount==None:
            final_num.append(num)
        else:
            final_num.append(amount)
    if ptf=='YES':
        for code,num in zip(codes_jq,final_num):
            print(f'比较后的股票:{code},数量:{num}')

    #实际交易
    slip_pct=0.01#滑点百分比
    slip=0.95#固定滑点
    quotation=easyquotation.use('sina')
    act=input('按任意键推出，Y/y继续下单！！！')
    if act=='Y' or act== 'y':
        #先卖出
        for code,num in zip(codes_jq,final_num):
            stock_info=quotation.real(code[:6])#查询股票的价格信息,easyquotation查股票只要6位数字
            now=stock_info[code[:6]]['now']#当前价格
            if num==0:
                if ptf=='YES':
                    print(f'{code}数量为0，不做买卖')
            elif '-' in str(num):#卖出
                num=abs(num)
                price=now*(1-slip_pct)#卖出价比当前价低，便于卖出
                price=round(price,2)
                order('SELL','',code,price,num)
                if ptf=='YES':
                    print(f'正在卖出股票{code},价格:{price},数量:{num}')

        #再买入
        for code,num in zip(codes_jq,final_num):
            stock_info=quotation.real(code[:6])#查询股票的价格信息,easyquotation查股票只要6位数字
            now=stock_info[code[:6]]['now']#当前价格
            if '-' not in str(num):#买入
                price=now*(1+slip_pct)#买入价比当前价高，便于买入
                price=round(price,2)
                order('BUY','',code,price,num)
                if ptf=='YES':
                    print(f'正在买入股票{code},价格:{price},数量:{num}')
    


###保持会话cookie
def keep_alive():
    # 业务码：301509=今日成交 | 301501=买入 | 301502=卖出 | 301504=账户信息 | 301503=持仓明细 | 301511=历史成交 |301508=当日委托
    #301510=历史委托
    BIZCODE = "301504"
    

    # 生成合法post data
    post_data = build_post_data(BIZCODE, PARAM)
    print("✅ 生成合法post data成功")

    # 发送请求
    url = "https://h5jy.gszq.com/servlet/call"

    count=1
    while True:
        count+=1
        response = requests.post(url, headers=HEADERS, data=post_data)
        print('count:',count)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
        time.sleep(random.randint(120,180))#3-4分钟内随机

###菜单
def Menu():
    choice=input('ap:acount & position\npos:position\nlscj:历史成交\njrcj:今日成交\nact.帐户信息\njrwt:今日委托\nlswt:历史委托\nt:做T\nbuys:等权重买入一组股票\nsells:清仓列明表中持有的股票\nsync:同步jq组合\ncs:检查状态')
    if choice=='ap':
        pass
    elif choice=='pos':
        BIZCODE = "301503"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
#        print("返回内容:", response.text)
        res=response.json()#转化为dick
        res=res['results'][0]
        print('='*20+'output'+'='*20)
        for i in res.keys():
            print(i,res[i])
    elif choice=='lscj':
        BIZCODE = "301511"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
#        print("返回内容:", response.text)
        res=response.json()#转化为dick
        res=res['results'][0]
        print('='*20+'output'+'='*20)
        for i in res.keys():
            print(i,res[i])
    elif choice=='jrcj':
        BIZCODE = "301509"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
    elif choice=='act':
        BIZCODE = "301504"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
#        print("返回内容:", response.json())#调试用
#        print(type(response.json()))#调试用
        res=response.json()#转化为dict
        res=res['results'][0]
        print('='*20+'output'+'='*20)
        for i in res.keys():
            print(i,res[i])
    elif choice=='buy':
        stock_code=input('请输入股票代码：')
        price=input('请输入价格：')
        amount=input('请输入数量：')
        response=order('buy',stock_code,price,amount)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
        """
        exchange_type=''
        entrust_bs="0"
        if 'sz' in stock_code.lower():
            stock_account=stock_S
            exchange_type="0"
        elif 'sh' in stock_code.lower():
            stock_account=stock_A
            exchange_type="2"
        BIZCODE = "301501"
        BUY_PARAM = {
        "entrust_way": "6",
        "branch_no": "301",
        "fund_account": account,  # 替换成你的资金账号
        "cust_code": account,     # 替换成你的客户代码
        "password": password,
        "session_id": "",
        "entrust_bs":entrust_bs,#买卖不同，好像买是0,卖是1
        "exchange_type":exchange_type,            # 2=沪市 0=深市
        "stock_account":stock_account,#沪市深市帐号不同
        "stock_code":stock_code,#大小写不敏感
        "entrust_price":price,
        "entrust_amount":amount,
        "userID":"DID",
        "business_version":"2",
        "wid": wid,
        "sysnode_id": "2",
        "op_station": f"2| | | | |{phone}| |wechat|2.0.1| | | | | |Android| | | ",
        "_t":str(int(time.time()))
        }
        post_data = build_post_data(BIZCODE, BUY_PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        """
    elif choice=='sell':
        stock_code=input('请输入股票代码：')
        price=input('请输入价格：')
        amount=input('请输入数量：')
        response=order('buy',stock_code,price,amount)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
        """
        entrust_bs="1"#卖出
        if 'sz' in stock_code.lower():
            stock_account=stock_S
            exchange_type="0"
        elif 'sh' in stock_code.lower():
            stock_account=stock_A
            exchange_type="2"
        BIZCODE = "301502"
        SELL_PARAM = {
        "entrust_way": "6",
        "branch_no": "301",
        "fund_account": account,  # 替换成你的资金账号
        "cust_code": account,     # 替换成你的客户代码
        "password": password,
        "session_id": "",
        "entrust_bs":entrust_bs,#买卖不同，好像买是0,卖是1
        "exchange_type":exchange_type,            # 2=沪市 0=深市
        "stock_account":stock_account,#沪市深市帐号不同
        "stock_code":stock_code,#大小写不敏感
        "entrust_price":price,
        "entrust_amount":amount,
        "userID":"DID",
        "business_version":"2",
        "wid": wid,
        "sysnode_id": "2",
        "op_station": f"2| | | | |{phone}| |wechat|2.0.1| | | | | |Android| | | ",
        "_t":str(int(time.time()))
        }
        post_data = build_post_data(BIZCODE, SELL_PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
        """
    elif choice=='jrwt':
        BIZCODE = "301508"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
    elif choice=='lswt':
        BIZCODE = "301510"
        post_data = build_post_data(BIZCODE, PARAM)
        response = requests.post(url, headers=HEADERS, data=post_data)
        print("状态码:", response.status_code)
        print("返回内容:", response.text)
    elif choice=='t':
        pass
    elif choice=='revoke':
        pass
    elif choice=='buys':
        pass
    elif choice=='sells':
        pass
    elif choice=='sync':
        passs
    elif choice=='cs':
        keep_alive()
    elif choice=='gd':
        file=input('请输入文件路径:')
        file=file.replace('\'','')
        get_data(file,'YES')


# ------------------------- 调用示例：自由查询/买卖 -------------------------
if __name__ == "__main__":
    Menu()
