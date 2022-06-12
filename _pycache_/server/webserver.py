from socket import *
import sys 
import os
import time
import datetime
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 8080
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

atime = (datetime.datetime.fromtimestamp(os.path.getmtime("helloworld.html"))).strftime("%Y %m %d %H %M %S")
mtime = int(os.path.getmtime("helloworld.html"))
print("Ready to serve...")
while True:
    connectionSocket, addr = serverSocket.accept()
    try:
        # print('Received a connection from: ', addr)
        time_start = time.clock()
        message = connectionSocket.recv(2048).decode()
        filename = (message.split()[1])[1:] 
        f = open(filename)
        outputdata = f.read()

        OkMSG = "HTTP/1.1 200 OK\r\n"
        dataMSG = "Last-Modified:"+str(mtime)+"\r\n\r\n"
        # print(dataMSG)
        sendData = OkMSG+dataMSG+ outputdata
        connectionSocket.sendall(sendData.encode())

        time_end = time.clock()
        time_c= time_end - time_start
        print("GET /"+filename + "\033[1;32m 200 \033[0m" + str(round(time_c*1000,3)) + "ms");
        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        time_start = time.clock()
        ErrMSG = 'HTTP/1.1 404 Not Found \r\n\r\n'
        connectionSocket.send(ErrMSG.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()
        time_end = time.clock()
        time_c= time_end - time_start
        print("GET /"+filename + "\033[1;31m 404 \033[0m" + str(round(time_c*1000,3)) + "ms");
        connectionSocket.close()


serverSocket.close()
sys.exit()

