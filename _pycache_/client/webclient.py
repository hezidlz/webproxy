import sys
from socket import *
import time


serverName='127.0.0.1' 
serverPort=6789 
now = int (time.time())
checkInterval, filename = sys.argv[1:3]

request_head_1='GET /'
request_head_2=' HTTP/1.1\nHost: 127.0.0.1:48\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\n\
Purpose: prefetch\n\
Accept-Encoding: gzip, deflate, br\n\
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\nCheck-Interval: '+checkInterval+'\n'+ 'Request-Time: '+str(now)
request_head=request_head_1+filename+request_head_2

clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort)) 
clientSocket.send(request_head.encode()) 
mod=clientSocket.recv(1024)
print(mod.decode())

clientSocket.close()