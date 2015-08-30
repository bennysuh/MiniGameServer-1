import threading
from socket import *
import re
import Queue

class Pawn(object):
    def __init__(self, recvSock, clientAddr, clientRecvPort):
        self.recvSock = recvSock
        self.sendSock = self.connectToClient( clientAddr[0],clientRecvPort)
        self.msgQueue = Queue.Queue()
        
        
    def connectToClient(self, ip, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((ip, port))
        return sock
    
    def AsycFromClient(self):
        
        pass
    
    def AsycToClient(self):
        
        
        
        