import json,os,base64,time,random
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
stock_A=conf.get("gszq","stock_A")
stock_S=conf.get("gszq","stock_S")
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


###保持会话cookie
def keep_alive():
    # 业务码：301509=今日成交 | 301001=买入 | 301002=卖出 | 301504=账户信息 | 301503=持仓明细 | 301511=历史成交 |301508=当日委托
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
        res=response.json()#转化为dick
        res=res['results'][0]
        print('='*20+'output'+'='*20)
        for i in res.keys():
            print(i,res[i])
    elif choice=='buy':
        stock_code=''
        price=''
        amount=''
        exchange_type=''
        entrust_bs="0"
        stock_account=''
        BUY_PARAM = {
        "entrust_way": "6",
        "branch_no": "301",
        "fund_account": account,  # 替换成你的资金账号
        "cust_code": account,     # 替换成你的客户代码
        "password": password,
        "session_id": "",
        "entrust_bs":entrust_bs,#买卖不同，好像买是0,卖是1
        "exchange_type": "0",            # 2=沪市 0=深市
        "stock_account":stock_account,#沪市深市帐号不同
        "stock_code":stock_code,
        "entrust_price":price,
        "entrust_amount":amount,
        "userID":"DID",
        "business_version":"2",
        "wid": wid,
        "sysnode_id": "2",
        "op_station": f"2| | | | |{phone}| |wechat|2.0.1| | | | | |Android| | | ",
        "_t":str(int(time.time()))
        }
    elif choice=='sell':
        pass
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


# ------------------------- 调用示例：自由查询/买卖 -------------------------
if __name__ == "__main__":
    Menu()
