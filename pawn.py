import threading
from socket import *
import re
import Queue

class Pawn(object):
    def __init__(self, recvSock, clientAddr, clientRecvPort):
        self.recvSock = recvSock
        self.clientAddr = clientAddr
        self.sendSock = self.connectToClient( clientAddr[0],clientRecvPort)
        self.msgQueue = Queue.Queue()
        
        
    def connectToClient(self, ip, port):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((ip, port))
            print "conneted to client scuuess"
            return sock
        except Exception:
            print "connect to client %s error: %s"%(self.clientAddr ,str(Exception))
            return None
    
    def AsycFromClient(self):
        
        pass
    
    def AsycToClient(self):
        pass
        
        
        