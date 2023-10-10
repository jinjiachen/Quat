
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
from notification import notify
from notification import load_config


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


def login():
    url='https://joinquant.com/'
    username=''
    passwd=''
    driver.get(url)
    driver.find_element(By.XPATH,'//button[@class="banner-login show-dialog-login"]').click()#点击登录
    time.sleep(1)
    driver.find_element(By.XPATH,'//input[@name="CyLoginForm[username]"]').send_keys(username)
    driver.find_element(By.XPATH,'//input[@name="CyLoginForm[pwd]"]').send_keys(passwd)
    driver.find_element(By.XPATH,'//button[@class="login-submit btnPwdSubmit"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//button[@class="el-button menu-credit-button el-button--info is-disabled"]').click()#签到
    center='https://joinquant.com/view/user/floor?type=creditsdesc'
    comm_url='https://www.joinquant.com/view/community/list?listType=1'
    topic='https://www.joinquant.com/view/community/detail/8e16876acc72b895749564e4fc563621?type=1'#被选中的文章
    driver.get(topic)#阅读文章
    driver.get(center)#回到积分中心

if __name__ == '__main__':
    driver=Driver()
    login()
