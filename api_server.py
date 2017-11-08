import socket 
import time as Time
from threading import Thread,Event 


# :@author ATISH
# date:NOV-09-2017



class ServerThread(Thread): 

    def __init__(self,ip,port,csock,id,url,data): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.csock = csock
        self.id = id
        self.url = url
        self.data = data
        self.msg_list = {}
        self.msg = 'HTTP/1.0 200 OK\n\n'
        self.finished = Event()
        print( "[+] New server client connection started for " + ip + ":" + str(port)) 

    def stop (self):
            self.finished.set()
            self.msg_list['status']='killed'
            self.csock.send(self.msg.encode())
            self.csock.send(str(self.msg_list).encode())
            self.csock.close() 

    def run(self):
        print(self.url)
        if "GET" in self.url:
            if "api/request" in self.url:
                try:
                    l=self.url.split('?')
                    print (True)
                    if len(l)>1:
                        print(l[1])
                        data=l[1].split(' ')
                        print(data)
                        data=data[0].split('&')
                        print(data)
                        conn=data[0].split('=')
                        time=data[1].split('=')
                        connId=int(conn[1])
                        timeOut=int(time[1])
                        if connId not in connected_client:
                            connected_client[connId]=[Time.time(),timeOut,self.id]
                        print(connected_client)
                        Time.sleep(timeOut)
                        self.msg_list['status']='ok'
                        print(connId,timeOut)
                        print("connected_clients",str(connected_client))
                        del connected_client[connId]
                except:self.msg_list['error']="required parameter missing"
            elif "api/serverStatus" in self.url:
                for conn in connected_client:
                    print(conn)
                    self.msg_list[conn]=connected_client[conn][1]-int(Time.time()-connected_client[conn][0])
            else:
                self.msg_list['error']="path not correct"
        elif "PUT" in self.url:
            print("put request")
            print(self.url)
            print(self.data)
            try:
                if "/api/kill" in self.url:
                    connId = self.data.split(':')
                    connId = connId[1].split('}')
                    connId = int(connId[0])
                    print(connId,str(connected_client))
                    if connId in connected_client:
                        client_id = connected_client[connId][2]
                        print(client_id)
                        if clients_list[client_id].isAlive():
                            clients_list[client_id].stop()
                            del connected_client[connId]
                            self.msg_list['status']='ok'
                            print("thread stopped")
                    else:
                        self.msg_list['status']="invalid connection Id:"+str(connId)
                else:
                    self.msg_list['error']="path not correct"
            except:
                self.msg_list['error']="required  parameter missing"
            print(connected_client)
        else :
            self.msg_list['error']='this http method not define'   
        self.csock.send(self.msg.encode())
        self.csock.send(str(self.msg_list).encode())
        self.csock.close() 

HOST = '' 
PORT = 8080
BUFFER_SIZE = 20

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((HOST, PORT)) 
clients_list = [] 
connected_client={}# data of active request from client
id=0
while True: 
    server.listen(4)
    (csock, (ip,port)) = server.accept()
    data = csock.recv(4096)
    data = data.decode().split('\n')
    print(data)
    new_client = ServerThread(ip,port,csock,id,data[0],data[-1]) 
    new_client.start()
    clients_list.append(new_client)
    id=id+1

