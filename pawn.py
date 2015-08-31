import threading
from socket import *
import re
import Queue

class Pawn(object):
    def __init__(self, recvSock, sendSock):
        self.recvSock = recvSock
        self.sendSock = sendSock
        self.msgQueue = Queue.Queue()
        
    
    def AsycFromClient(self):
        
        pass
    
    def AsycToClient(self):
        pass
        
        
        