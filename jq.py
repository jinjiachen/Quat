
#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2023-10-10
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#import pyautogui
from lxml import etree
import urllib
import requests
import os
import time
import base64
import random,cv2
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
#    options = webdriver.ChromeOptions()#适用3.8以下
    options = Options()
#    options.add_argument("--proxy-server=http://192.168.2.108:8889")
    options.add_argument("--no-proxy-server")
#    options.add_argument("--headless")
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"')
#    options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"')
#    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')
    options.add_argument('log-level=3') #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
#    Chrome的驱动和路径
#    path="C:\Program Files\Google\Chrome\Application\chrome.exe"
#    driver=webdriver.Chrome(chrome_options=options,executable_path=path)
#    driver=webdriver.Chrome(path,chrome_options=options)
    driver=webdriver.Chrome(options=options)
    driver.maximize_window()
    #driver.set_page_load_timeout(10)
    #driver.set_script_timeout(10)
    print('starting')
    return driver


###关闭当前标签并返回最新标签
def close_update(driver):
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])#切换当前标签
    driver.close()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])#切换当前标签
    return driver



def login(driver,username,passwd,dry_run='NO'):
    url='https://joinquant.com/'
    driver.get(url)
    time.sleep(3)
    #进行登录
    driver.find_element(By.XPATH,'//button[@class="banner-login show-dialog-login"]').click()#点击登录
    time.sleep(1)
    driver.find_element(By.XPATH,'//input[@name="username"]').send_keys(username)
    driver.find_element(By.XPATH,'//input[@name="pwd"]').send_keys(passwd)
    driver.find_element(By.XPATH,'//input[@id="agreementBox"]').click()#勾选协议
    driver.find_element(By.XPATH,'//button[@class="login-submit btnPwdSubmit"]').click()
    time.sleep(1)
    #driver.switch_to.default_content()
#    slider=driver.find_element(By.XPATH,'//div[@id="drag"]')
#    ActionChains(slider).drag_and_drop_by_offset(slider,100,0)
#    ActionChains(slider).perform()
#    driver.find_element(By.XPATH,'//div[@class="bootstrap-dialog-close-button"]/button').click()
    time.sleep(10)


    if dry_run=='NO':
        try:
            action=ActionChains(driver)
            driver.find_element(By.XPATH,'//button[@class="el-button menu-credit-button el-button--primary"]').click()#签到
#            driver.find_element(By.XPATH,'//div[@aria-label="完成拼图验证"]/div/button').click()#关闭验证
            time.sleep(1)
            driver.save_screenshot('shot.png')#屏幕截图,必须为png
            print('截图成功')
            handle=driver.find_element(By.XPATH,'//div[@aria-label="完成拼图验证"]/div[2]//div[@id="drag"]/div[3]')#滑块位置
#            handle=driver.find_element(By.XPATH,'//div[@class="valid-code__drag"]')#拖动的滑块,此法无效
            #click and hold方法可行，drag and hold不行，不知为何
            action.click_and_hold(handle)
            action.move_by_offset(100,0)
            action.release()
        #    action.move_to_element(handle)
        #    action.drag_and_drop_by_offset(handle,10,0)
            action.perform()
            time.sleep(2)
            print(f'{username}签到成功')
        except:
            print('签到失败')
            
    picture_mark('shot.png')
    picture_scrot('shot.png',(760,240),(1230,455))
    #获取阅读文章积分
    center='https://joinquant.com/view/user/floor?type=creditsdesc'
    driver.get(center)#回到积分中心
    time.sleep(1)
    try:
        driver.find_element(By.XPATH,'//a[@href="/./view/community/list?listType=1"]/button').click()#去看看
    except:
        print('已经领取过阅读积分')
    windows = driver.window_handles
    driver.switch_to.window(windows[1])#切换第二个标签
    comm_url='https://www.joinquant.com/view/community/list?listType=1'
    time.sleep(5)

    num=len(driver.find_elements(By.XPATH,'//div[@class="jq-c-list_community__text"]'))#获取主题的数量
    i=random.randint(3,num)
    print(f'主题总数：{num},阅读随机文章{i}')
    time.sleep(1)
    driver.find_elements(By.XPATH,'//div[@class="jq-c-list_community__text"]')[i-1].click()#随机点击文章查看
    time.sleep(9)
    driver=close_update(driver)
    driver.get(center)#回到积分中心
    time.sleep(3)
    if dry_run=='NO':
        try:
            driver.find_element(By.XPATH,'//button[@class="el-button el-button--primary el-button--mini"]').click()#领取阅读积分
            time.sleep(1)
            print(f'{username}领取阅读积分')
        except:
            print('领取失败')
            
#    point=driver.find_element(By.XPATH,'//div[@class="jq-user-floor__div-item"][1]/text()')
#    print(f'当前积分{point}')
    #关闭多余标签
#    while True:
#        windows = driver.window_handles
#        if len(windows)==1:
#            driver.switch_to.window(windows[-1])#切换当前标签
#            break
#        else:
#            driver.switch_to.window(windows[-1])#切换当前标签
#            driver.close()
        
    driver.quit()


def auto_check():
    conf=load_config()
    accounts=conf.options('jq')#获取jq这个section下的items
#    print(accounts)#调试用
    for item in accounts:
        driver=Driver()
        print(f'正在处理{item}')
        token=conf.get('jq',item)
        string=base64.b64decode(token).decode('ascii')
        string=string.split(' ')
        username=string[0]
        passwd=string[1]
        login(driver,username,passwd,dry_run='NO')


###识别缺口的位置
def identify_gap(yz,qk):
    '''
    yz(str):验证的图片
    qk(str):移动的缺口图片
    '''
    yz_img=cv2.imread(yz)#加载验证图片
    qk_img=cv2.imread(qk)#加载缺口图片
    dirname=os.path.dirname(yz)

    #识别图片边缘
    yz_canny=cv2.Canny(yz_img,100,200)
    qk_canny=cv2.Canny(qk_img,100,200)
    #缺口的匹配
    res=cv2.matchTemplate(yz_canny,qk_canny,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)

#    th,tw=yz_img.shape[:2]
    th,tw=qk_canny.shape[:2]
    tl=max_loc
    br=(tl[0]+tw,tl[1]+th)
    cv2.rectangle(yz_img,tl,br,(0,0,255),2)
    print(dirname)
#    cv2.imwrite(dirname+'\out1.jpg',yz_canny)
#    cv2.imwrite(dirname+'\out2.jpg',qk_canny)
#    cv2.imwrite(dirname+'\out3.jpg',yz_img)

    
###图像标记
def picture_mark(pic):
    '''
    pic(str):图片路径
    '''
    img=cv2.imread(pic)#加载验证图片
    print(img.shape)
    pt1=(650,130)
    pt2=(1270,590)
    cv2.rectangle(img,pt1,pt2,(0,0,255),2)
    pt3=(760,240)
    pt4=(1230,455)
    cv2.rectangle(img,pt3,pt4,(0,255,0),2)
#    print('图片修改')
    cv2.imwrite('shot_revise.png',img)
#    print('图片保存')

###图像裁剪
def picture_scrot(pic,corp1,corp2):
    '''
    pic(str):图片路径
    corp(tuple):裁剪的第一个坐标
    corp(tuple):裁剪的第二个坐标
    '''
    img=cv2.imread(pic)#加载验证图片
    scrot_img=img[corp1[1]:corp2[1],corp1[0]:corp2[0]]#截取的范围，y0:y1,x0:x1
    cv2.imwrite('scrot.png',scrot_img)


if __name__ == '__main__':
    auto_check()
#    yz=input('请输入验证图片')
#    qk=input('请输入缺口图片')
#    identify_gap(yz,qk)
