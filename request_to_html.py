import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def save_with_requests(url, save_name="page_requests.html"):
    """requests 方式抓取并保存网页"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    print(f"[1] 正在用 requests 抓取：{url}")
    resp = requests.get(url, headers=headers, timeout=15)
    resp.encoding = resp.apparent_encoding

    with open(save_name, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"✅ 保存成功：{save_name}")


def save_with_selenium(url, save_name="page_selenium.html"):
    """Selenium 真实浏览器抓取（支持动态JS）"""
    print(f"[2] 正在用 Selenium 抓取：{url}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 后台运行，不弹出浏览器
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.page_source
    driver.quit()

    with open(save_name, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 保存成功：{save_name}")


def menu():
    print("====== 网页保存工具 ======")
    print("1 → requests 方式（快，轻量）")
    print("2 → Selenium 方式（真浏览器，能抓动态页面）")
    choice = input("请选择抓取方式（1/2）：")

    url = input("请输入要抓取的网址：")
    if not url.startswith("http"):
        url = "https://" + url

    if choice == "1":
        save_with_requests(url)
    elif choice == "2":
        save_with_selenium(url)
    else:
        print("❌ 输入错误，请输入 1 或 2")


if __name__ == "__main__":
    menu()
