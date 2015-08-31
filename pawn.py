import threading
from socket import *
import re
import Queue
from msgparser import *
import time

BUF_SIZE = 2048
class Pawn(object):
    def __init__(self, recvSock, sendSock, msgQueue):
        self.recvSock = recvSock
        self.sendSock = sendSock
        self.msgQueue = msgQueue
        self.recvFlagQueue = Queue.Queue()
        self.sendFlagQueue = Queue.Queue()
        self.msgParser = MsgParser()
        self.sendMsgQueue = Queue.Queue()
    
    def AsycFromClient(self):
        
        pass
    
    def AsycToClient(self):
        pass
    
    def StartRecvThread(self):
        print "Operation: StartRecvThread"
        self.StopRecvThread()
        self.recvFlagQueue.put(True)
        t = threading.Thread(target = self.KeepRecvFromClient, args = ())
        t.start()
        
    def StopRecvThread(self):
        print "Operation: StopRecvThread"
        if self.recvFlagQueue.qsize()>0:
            self.recvFlagQueue.get()
            print "Stop successfully...."
        else:
            print "Thread was already stopped....."
          
    def StartSendThread(self):
        print "Operation: StartSendThread"
        self.StopSendThread()
        self.sendFlagQueue.put(True)
        t = threading.Thread(target = self.KeepSendToClient, args = ())
        t.start()
        
    def StopSendThread(self):
        print "Operation: StopSendThread"
        if self.sendFlagQueue.qsize()>0:
            self.sendFlagQueue.get()
            print "Stop successfully...."
        else:
            print "Thread was already stopped....."
        
            
        
    def KeepRecvFromClient(self):
        print "RecvThread start"
        while True and self.recvFlagQueue.qsize() > 0:
            data = self.recvSock.recv(BUF_SIZE)
            self.msgParser.parseMsg(data)
            self.msgQueue.put(data)
            time.sleep(0.05)
        print "RecvThread end"
            
    def Send(self, msg):
        self.sendMsgQueue.put(msg)
        
    def KeepSendToClient(self):
        print "SendThread start"
        while True and self.sendFlagQueue.qsize() > 0:
            if self.sendMsgQueue.qsize() > 0:
                self.sendSock.sendall(self.sendMsgQueue.get())
            time.sleep(0.05)
        print "SendThread end"
            
        
        