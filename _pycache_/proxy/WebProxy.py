#coding:utf-8
from socket import *
import os
import time
# 创建socket，绑定到端口，开始监听
tcpSerPort = 6789
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)
now = int (time.time())

while True:
    # 从客户端接收请求
    print("Ready to serve...")
    tcpCliSock, addr = tcpSerSock.accept()
    print('---Received a connection from: ', addr)
    message = tcpCliSock.recv(4096).decode()
    requestTime = message[-10:]
    checkInteval = int((((message.split("\n"))[-2]).split(":"))[-1])
    filename = (message.split()[1])[1:] 
    OkMSG = "HTTP/1.1 200 OK\r\n\r\n"
    try:
        # 检查缓存中是否存在该文件
        f = open(filename, "r")
        print("---file exist in cache!")
        outputdata = f.read()
        createTime = int(os.path.getmtime(filename))
        diff = int(requestTime) - createTime

        # 时间差大于检查时间,进行conditional get
        if diff > checkInteval:
            print("---time interval greater than the preset value, Let's go to conditional get!")
            c = socket(AF_INET, SOCK_STREAM)
            c.connect(('127.0.0.1', 8080))
            c.send(message.encode())
            buff = c.recv(4096)
            serverCreateTime = int((buff.decode().split("\n")[1]).split(":")[1])
            # 文件在server端未被更新
            if createTime >= serverCreateTime :
                print("---the requested file is the newest!")
                sendData = OkMSG+ outputdata
                tcpCliSock.sendall(sendData.encode())
                os.utime(filename,(now,now))
                print("---Read from cache!\n")

            # 文件在server端被更新
            else:
                print("---the requested file is old, let's send request to server!")
                writeData = "\n".join((buff.decode().split("\n"))[3:])
                tmpFile = open("./" + filename, "w")
                tmpFile.write(writeData)
                tmpFile.close()
                f = open(filename, "r")
                outputdata = f.read()
                sendData = OkMSG+ outputdata
                tcpCliSock.sendall(sendData.encode())
                print("---Read from server!\n")

        #时间差小于检查时间,直接返回
        else :
            print("---time interval less than the preset value, let's return immediately")
            os.utime(filename,(now,now))
            sendData = OkMSG+ outputdata
            tcpCliSock.sendall(sendData.encode())
            print("---Read from cache!\n")

    # 缓存中不存在该文件，异常处理
    except IOError:
        print('---File not Exist in cache!')
        c = socket(AF_INET, SOCK_STREAM)
        c.connect(('127.0.0.1', 8080))
        c.send(message.encode())
        buff = c.recv(4096)
        status = (buff.decode().split())[1]
        # 文件存在
        if(status=="200"):
            print('---file exists in server!')
            fileData = "\n".join((buff.decode().split("\n"))[3:])
            tmpFile = open("./" + filename, "w")
            tmpFile.write(fileData)
            tmpFile.close()
            f = open(filename, "r")
            outputdata = f.read()
            sendData = OkMSG+ outputdata
            tcpCliSock.sendall(sendData.encode())
            print("---Read from server!\n")
        else:
            ErrMSG = 'HTTP/1.1 404 Not Found \r\n\r\n'
            print("---file not exist in server\n")
            tcpCliSock.sendall(ErrMSG.encode())
    tcpCliSock.close()
tcpSerSock.close()