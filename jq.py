
#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-10-10
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
from lxml import etree
import urllib
import requests
import os
import time
import base64
from configparser import ConfigParser
from notification import notify
from notification import load_config


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

def Driver():
    #Chrom的配置
    options = webdriver.ChromeOptions()
#    options.add_argument("--proxy-server=http://192.168.2.108:8889")
#    options.add_argument("--no-proxy-server")
#    options.add_argument("--headless")
#    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"')
#    options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"')
#    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')
    options.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
#    Chrome的驱动和路径
#    path="C:\Program Files\Google\Chrome\Application\chrome.exe"
#    driver=webdriver.Chrome(chrome_options=options,executable_path=path)
#    driver=webdriver.Chrome(path,chrome_options=options)
    driver=webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    #driver.set_page_load_timeout(10)
    #driver.set_script_timeout(10)
    print('starting')
    return driver


def login(driver,username,passwd):
    url='https://joinquant.com/'
    driver.get(url)
    time.sleep(3)
    #进行登录
    driver.find_element(By.XPATH,'//button[@class="banner-login show-dialog-login"]').click()#点击登录
    time.sleep(1)
    driver.find_element(By.XPATH,'//input[@name="CyLoginForm[username]"]').send_keys(username)
    driver.find_element(By.XPATH,'//input[@name="CyLoginForm[pwd]"]').send_keys(passwd)
    driver.find_element(By.XPATH,'//button[@class="login-submit btnPwdSubmit"]').click()
    time.sleep(1)

#    driver.find_element(By.XPATH,'//button[@class="el-button menu-credit-button el-button--primary"]').click()#签到
    #获取阅读文章积分
    center='https://joinquant.com/view/user/floor?type=creditsdesc'
    driver.get(center)#回到积分中心
    time.sleep(1)
    driver.find_element(By.XPATH,'//a[@href="/./view/community/list?listType=1"]/button').click()
    windows = driver.window_handles
    driver.switch_to.window(windows[1])#切换第二个标签
    comm_url='https://www.joinquant.com/view/community/list?listType=1'
    time.sleep(2)

    driver.find_element(By.XPATH,'//div[@class="jq-c-list_community__text"]').click()#点击文章查看
    time.sleep(5)
    driver.execute_script("window.scrollBy(0,10000)")
    time.sleep(5)
    driver.execute_script("window.scrollBy(10000,0)")
    time.sleep(5)
    driver.execute_script("window.scrollBy(0,10000)")
    driver.get(center)#回到积分中心
    time.sleep(5)
#    driver.find_element(By.XPATH,'//button[@class="el-button el-button--primary el-button--mini"]').click()#领取阅读积分
    #关闭多余标签
    while True:
        windows = driver.window_handles
        if len(windows)==1:
            driver.switch_to.window(windows[-1])#切换当前标签
            break
        else:
            driver.switch_to.window(windows[-1])#切换当前标签
            driver.close()
        
        
    

if __name__ == '__main__':
    driver=Driver()
    conf=load_config()
    accounts=conf.options('jq')#获取jq这个section下的items
#    print(accounts)
    for item in accounts:
        print(f'正在处理{item}')
        token=conf.get('jq',item)
        string=base64.b64decode(token).decode('ascii')
        string=string.split(' ')
        username=string[0]
        passwd=string[1]
        login(driver,username,passwd)
