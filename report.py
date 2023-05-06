#!/bin/python
#coding=utf8
'''
Author: Michael Jin
Date: 2024-04-20
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import etree
import urllib
import requests
import os
import time

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


def sse():
    url='http://www.sse.com.cn/disclosure/listedinfo/regular/'
    driver.get(url)
    time.sleep(3)
    #以下是报告时间段的选择
    driver.find_element(By.XPATH,'//input[@class="form-control sse_input"]').click()
    driver.find_element(By.XPATH,'//div[@id="layui-laydate1"]/div[1]//td[@class="layui-this"]').click()#开始日期
    driver.find_element(By.XPATH,'//div[@id="layui-laydate1"]/div[2]//i[@class="layui-icon laydate-icon laydate-prev-m"]').click()#往前一个月
    driver.find_element(By.XPATH,'//div[@id="layui-laydate1"]/div[2]//td[@class="layui-this"]').click()#结束日期
    driver.find_element(By.XPATH,'//span[@lay-type="confirm"]').click()#确定

    time.sleep(2)
    html=driver.page_source
    selector=etree.HTML(html)
    info=selector.xpath('//tbody/tr/td//text()')
    print(info)


if __name__ == '__main__':
    driver=Driver()
    sse()
