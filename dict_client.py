# from socket import *
# import time

# sockfd=socket()
# sockfd.connect('0.0.0.0',8888)
# while True:
#     input=msg('请输入要查询的单词：')
#     sockfd.send(input.encode())
#     data=sockfd.recv(1024).decode()
#     print(data)
# sockfd.close()


#!/usr/bin/python3
#coding=utf-8

from socket import *
import sys
import getpass

# 创建网络连接
def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    s=socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            ============Welcome============
            --1.注册　　　2.登录　　　３．退出
            ===============================
            ''')
        try: 
            cmd=int(input('输入选项>>'))
        except Exception as e:
            print(e)
            continue
        if cmd not in [1,2,3]:
            print('请输入正确的选项')
            sys.stdin.flush()  #清楚标准输入
        elif cmd==1:
            r=do_register(s)
            if r==0:
                print('注册成功')
                # login(s,name)
            if r==1:
                print('用户存在')
            if r==2:
                print('注册失败')

        elif cmd==2:
            name=do_login(s)
            if name:
                print('登录成功')
                login(s,name)

            else:
                print('登录失败')

        elif cmd==3:
            s.send(b'E')
            sys.exit('谢谢使用')



def do_login(s):
    while True:
        name=input('请输入姓名：')
        passwd=input('请输入密码：')
        msg='L {} {}'.format(name,passwd)
        s.send(msg.encode())
        data=s.recv(1024).decode()
        if data=='OK':
            return name
        else:
            return









def do_register(s):
    while True:
        name=input('User:')
        passwd=getpass.getpass()
        passwd1=getpass.getpass('Again:')
        if (' ' in name )or (' ' in passwd):
            print('用户名和密码不许有空格')
        if passwd!=passwd1:
            print('两次密码不一致')
            continue
        msg='R {} {}'.format(name,passwd)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data=s.recv(1024).decode()
        if data=='OK':
            return 0
        elif data=='EXISTS':
            return 1
        else:
            return 2

def login(s,name):
    while True:
        print('''
                ===========查询界面=============
                １．查词　　２．历史记录　　３．退出
                ===============================
            ''')
        try: 
            cmd=int(input('输入选项>>'))
        except Exception as e:
            print(e)
            continue
        if cmd not in [1,2,3]:
            print('请输入正确的选项')
            sys.stdin.flush()  #清除标准输入
            continue
        elif cmd==1:
            do_query(s,name)
        elif cmd==2:
            do_hist(s,name)
        elif cmd==3:
            return
# 查单词
def do_query(s,name):
    while True:
        word=input('单词：')
        if word=='##':
            break
        msg="Q {} {}".format(name,word)
        s.send(msg.encode())
        data=s.recv(1024).decode()
        if data=='OK':
            print('查询成功！')
            data=s.recv(1024).decode()
            print(data)
        else:
            print('没有查到该单词')


def do_hist(s,name):
    msg='H {}'.format(name)
    s.send(msg.encode())
    data=s.recv(1024).decode()
    if data=='OK':
        while True:
            data=s.recv(1024).decode()
            if data=='##':
                break
            print('历史记录为：',data)
    else:
        print('没有该历史记录')

if __name__=='__main__':
    main()
