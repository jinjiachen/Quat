#!/bin/python
#coding=utf8
'''
Author: Michael Jin
date:2026-04-30
'''

import socket
from configparser import ConfigParser
import os


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

# -------------------------- 配置信息 --------------------------
conf=load_config()
REDIS_HOST=conf.get('redis','host')
REDIS_PORT=int(conf.get('redis','port'))
REDIS_PASSWORD=conf.get('redis','token')
CHANNEL = "xq"
# -------------------------------------------------------------

def redis_subscribe_socket():
    # 1. 创建原生 TCP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接 Redis 服务器
    sock.connect((REDIS_HOST, REDIS_PORT))
    print("✅ Socket 连接 Redis 成功")

    # 2. 发送 AUTH 命令（密码认证，必须遵循 RESP 协议）
    # RESP 协议格式：*参数数量\r\n$长度1\r\n值1\r\n$长度2\r\n值2\r\n
    auth_cmd = f"*2\r\n$4\r\nAUTH\r\n${len(REDIS_PASSWORD)}\r\n{REDIS_PASSWORD}\r\n"
    sock.send(auth_cmd.encode())
    auth_resp = sock.recv(1024).decode()
    if "+OK" not in auth_resp:
        print("❌ 密码认证失败")
        return
    print("✅ 密码认证成功")

    # 3. 发送 SUBSCRIBE 命令（订阅频道）
    sub_cmd = f"*2\r\n$9\r\nSUBSCRIBE\r\n${len(CHANNEL)}\r\n{CHANNEL}\r\n"
    sock.send(sub_cmd.encode())
    print(f"✅ 成功订阅频道：{CHANNEL}，等待实时消息...")

    # 4. 阻塞监听服务端主动推送的消息（核心：无轮询）
    while True:
        # 阻塞等待，服务端有消息会直接推送过来
        msg = sock.recv(1024).decode().strip()
        if not msg:
            break
        # 解析 Redis 推送的消息（RESP 协议格式）
        print(f"📩 收到实时推送：{msg}")

if __name__ == '__main__':
    redis_subscribe_socket()
