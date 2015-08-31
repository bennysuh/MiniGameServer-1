#_*_coding:gbk_*_

from socket import *
import re
from msgparser import *
from pawn import *
import time
import Queue
import threading
"""
msg format:


$TART$
$name:PAWN_NAME
$isDead:true
$growth:100
$pos:100,200
$END$
"""

msg1 = """$START$
$name:PAWN_NAME1$$$
$isDead:true$$$
$growth:100$$$
$pos:100,200$$$
$type:water$$$
$END$
$START$
$name:PAWN_NAME2$$$
$isDead:false$$$
$growth:100$$$
$pos:120,200$$$
$type:wood$$$
$END$

"""

mutex = threading.Lock()
pawnDic = {}
pawnList = []
pawnQueue = Queue.Queue()


      
            
msgParser = MsgParser()      
# msgParser.printMsg(msg1)
# print msgParser.parseToDict(msg1)

port = 10010
BUF_SIZE = 2048  
AD = ("0.0.0.0", port)
AD1 = ("0.0.0.0", port+1)
so = socket(AF_INET,SOCK_STREAM)
so.bind(AD)
so.listen(1000)
clientRecvSock = socket(AF_INET,SOCK_STREAM)
clientRecvSock.bind( AD1 )
clientRecvSock.listen(1000)

flagBrodcastQueue = Queue.Queue()
flagBrodcastQueue.put(True)
msgQueue = Queue.Queue()
def BrodCasting():
    print "broadCast Thread start"
    global pawnDic, pawnList, pawnQueue, flagQueue, mutex
    while True and flagBrodcastQueue.qsize() > 0:
        if True:
            
            tmpStr = ''
            if msgQueue.qsize() > 0:
                print "brodcast at ",time.ctime()
                print "msgQueue qsize :",msgQueue.qsize()
                for i in range(msgQueue.qsize()):
                    s = msgQueue.get()
                    if s=='' or s.find("$") < 0 :
                        continue
                    print i,"st str :",repr(s)
                    tmpStr += s
            if len(tmpStr) > 0:
                print "BroadCasting thread, sending"
                mutex.acquire()
                for p in pawnList:
                    p.send(tmpStr)
                mutex.release()
            
        time.sleep(0.1)
    print "broadCast Thread end"
broadCastThread = threading.Thread(target=BrodCasting, args = ())
broadCastThread.start()          

while True:
    print "waiting for connection..."
    client, addr = so.accept() 
    print "get connection from client....addr: ",str(addr)
    data = client.recv(BUF_SIZE)
    print msgParser.printMsg(data)
    tmpDic = msgParser.parseToDict(data)
    tmpDic = tmpDic[0]
    if tmpDic.has_key('name') and tmpDic.has_key('port'):
        
        #"""不存在此名字  视为服务器创建角色成功"""
        if not pawnDic.has_key(tmpDic['name']):
            print "%sSUCCESS%s"%(START,END)
            client.sendall("%sSUCCESS%s"%(START,END))
            sock1, addr1 = clientRecvSock.accept()
            sock1.sendall("%sSUCCESS%s"%(START,END))
            pawn = Pawn(client, sock1, msgQueue)
            pawn.StartRecvThread()
            pawn.StartSendThread()
            pawnDic[ tmpDic['name'] ] = pawn
            pawnList.append(pawn)
            pawnQueue.put(pawn)
            pass
        #"""存在此名字  服务器已经存在同名角色，返回错误"""
        else:
            print "%sERROR:name %s already exists....please rename...%s"%(START,tmpDic['name'],END)
            client.sendall("%sERROR:name %s already exists....please rename...%s"%(START,tmpDic['name'],END))
            
            pass
    else:
        print "data format cant be recognized...."
        print data
        pass
            
            
            
    

