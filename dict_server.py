# import os
# from time import sleep
# from socket import *

# l=[]
# while True:
#     pid=os.fork()

#     if pid<0:
#         print('创建进程失败')
#     if pid==0:
#         print('创建子进程成功')
#         sockfd=socket.decode()
#         sockfd.bind(('0.0.0.0',8888))
#         sockfd.listen(5)
#         connfd,addr=sockfd.accept()
#         print('connect from',addr)
#         l.append(connfd)
#         while True:
#             data=connfd.recv(1024).decode()
#             if data=='##':
#                 break
#             connfd.send('recieve your message'.encode())
#             sleep(0.5)
#         connfd.close()
#         sockfd.close()
#     else:
#         print('这是父进程')
# for i in l:
#     i.wait()




'''
name:Tedu
data:2018-10-1
email:xxx
modules:pymysql
this is project from aid
'''

from socket import *
import os
import time 
import signal
import pymysql
import sys

# 定义需要的全局变量
DICT_TEXT='./dict.txt'
HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)

# 流程控制
def main():

    # 创建数据库链接
    db=pymysql.connect('localhost','root','123456','dict')

    # 创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    # 忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            c,addr=s.accept()
            print('connect from ',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        pid=os.fork()
        if pid==0:
            s.close()
            do_child(c,db)
        else:
            c.close()
            continue

def do_child(c,db):
    while True:
        data=c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0]=='E':
            c.close()
            sys.exit(0)
        if data[0]=='R':
            do_register(c,db,data)
        if data[0]=='L':
            # print(data)
            do_login(c,db,data)
        if data[0]=='Q':
            do_query(c,db,data)
        if data[0]=='H':
            do_hist(c,db,data)

        print(data)

def do_login(c,db,data):
    print('登录操作')
    l=data.split(' ')
    print(l)
    name=l[1]
    passwd=l[2]
    cursor=db.cursor()
    sql="select * from user where passwd='%s'"%passwd
    cursor.execute(sql)
    r=cursor.fetchone()
    if r!=None:
        print('%s登录成功'%name)
        c.send(b'OK')
    else:
        print('密码错误')
        c.send(b'fail')
    # try:
    #     cursor.execute(sql)
    #     sq.commit()
    # except Exception as e:
    #     print(e)
    #     db.rollback()
    








def do_register(c,db,data):
    print('注册操作')
    l=data.split(' ')
    name=l[1]
    passwd=l[2]
    cursor=db.cursor()
    sql="select * from user where name='%s' and passwd='%s'"%(name,passwd)
    cursor.execute(sql)
    r=cursor.fetchone()

    if r!=None:
        c.send(b'EXISTS')
        return
    # 插入用户
    sql="insert into user (name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception as e:
        print(e)
        db.rollback()
        c.send(b'FALL')
    else:
        print('%s注册成功'%name)


def do_query(c,db,data):
    print('查询操作')
    l=data.split(' ')
    name=l[1]
    word=l[2]
    cursor=db.cursor()

    def insert_history():
        tm=time.ctime()
        sql="insert into hist(name,word,time)\
        values('%s','%s','%s')"%(name,word,tm)
        try:   
            cursor.execute(sql)
            db.commit()
            # print('插入历史记录成功')
        except Exception as e:
            print(e)
            db.rollback()


    # 文本查询
    try:
        f=open(DICT_TEXT)
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp=line.split(' ')[0]
        if tmp>word:
            c.send(b'FALL')
            f.close()
            return
        elif tmp==word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()



    # sql="select * from words where word='%s'"%word
    # try:
    #     query=cursor.execute(sql)
    #     db.commit()
    # except Exception as e:
    #     print(e)
    #     db.rollback()
    # r=cursor.fetchone()
    # if r!=None:
    #     print('单词库有该单词')
    #     c.send(b'OK')
    #     print(query,'===========')
    # else:
    #     print('没有该单词')
    #     c.send(b'fail')

def do_hist(c,db,data):
    print('查询历史记录')
    l=data.split(' ')
    name=l[1]
    sql="select * from hist where name='%s'"%name
    cursor=db.cursor()
    try:
        data=cursor.execute(sql)
        r=cursor.fetchall()
        db.commit()
        if r!=None:
            c.send(b'OK')
        else:
            c.send(b'FALL')
            return
        for i in r:
            time.sleep(0.1)
            msg='%s  %s  %s'%(i[1],i[2],i[3])
            c.send(msg.encode())
        time.sleep(0.1)
        c.send(b'##')


    except Exception as e:
        print(e)
        db.rollback()


if __name__=='__main__':
    main()



