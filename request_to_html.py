import requests

# 目标网址（你可以随便改）
url=input("请输入请求网址：")

# 发送请求，获取网页内容
response = requests.get(url)

# 设置编码（防止中文乱码，非常重要）
response.encoding = response.apparent_encoding

# 把网页保存为 html 文件
with open("saved_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("网页已保存为 saved_page.html")
