from socket import *
import re
from msgparser import MsgParser

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
msgParser.printMsg(msg1)
print msgParser.parseToDict(msg1)

print len('')
port = 10085
BUF_SIZE = 2048  
AD = ("0.0.0.0", port)
so = socket(AF_INET,SOCK_STREAM)
so.bind(AD)
so.listen(50)
while True:
    print "waiting for connection..."
    client, addr = so.accept() 
    print "connected....addr: "
    print str(addr)
    data = client.recv(BUF_SIZE)
    print data

