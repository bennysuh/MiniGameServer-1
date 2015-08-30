#_*_coding:gbk_*_

from socket import *
import re
from msgparser import *
from pawn import *
import time

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


        
            
msgParser = MsgParser()      
# msgParser.printMsg(msg1)
# print msgParser.parseToDict(msg1)

port = 10086
BUF_SIZE = 2048  
AD = ("0.0.0.0", port)
so = socket(AF_INET,SOCK_STREAM)
so.bind(AD)
so.listen(1000)

pawnDic = {}
pawnList = []
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
            time.sleep(0.2)
            pawn = Pawn(client, addr, int(tmpDic['port']))
            pawnDic[ tmpDic['name'] ] = pawn
            pawnList.append(pawn)
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
            
            
            
    

