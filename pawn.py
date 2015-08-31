import threading
from socket import *
import re
import Queue
from msgparser import *
import time
import select

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
            try:
                ready_to_read, ready_to_write, in_error = \
            select.select([self.recvSock,],[self.recvSock,], [], 0.2)
            except select.error:
                self.recvSock.shutdown(1)
                self.recvSock.close()
                break
            if len(ready_to_read) > 0: 
                data = self.recvSock.recv(BUF_SIZE)
                print "recv a msg, put to msgqueue...",data
                if data.find(APP_QUIT) > 0:
                    print "client app quit"
                    self.StopRecvThread()
                    self.StopSendThread()
                    self.recvSock.shutdown(1)
                    self.recvSock.close()
                    self.sendSock.shutdown(1)
                    self.sendSock.close()
                    break
                
                    
                if data.find(START) > 0:
                    
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
                try:
                    ready_to_read, ready_to_write, in_error = \
            select.select([self.sendSock,],[self.sendSock,], [], 0.2)
                except select.error:
                    self.sendSock.shutdown(1)
                    self.sendSock.close()
                    break
                if len(ready_to_write) > 0:
                    self.sendSock.send(self.sendMsgQueue.get())
            time.sleep(0.05)
        print "SendThread end"
            
        
        