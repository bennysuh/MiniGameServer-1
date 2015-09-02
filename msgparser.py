import re
import time
import threading
START = "$START$"
END = "$END$"
LINEEND = "$$$"
APP_QUIT="APP_QUIT"
attrs = ['name','isDead','growth','pos','type','port','vec','state']
mutexf = threading.Lock()
def myPrint(s, *args):
    global mutexf
    mutexf.acquire()
    f = open('python_log.log','w+')
    f.write(str(s)+str(args)+'\n')
    f.flush()
    f.close()
    mutexf.release()
    
    
class MsgParser(object):
    def __init__(self):
        pass
    
    def parseMsg(self,msg):
        global attrs, START, END, LINEEND
        msglist = []
        m = msg.split(START)
        for item in m:
        
            item = item.replace(START,'')
            item = item.replace(END,'')
            item = item.replace('\n','')
            if len(str(item)) > 0:
                msglist.append(item)
        return msglist
    def parseInfo(self,msglist):
        global attrs, START, END, LINEEND
        infolist = []
        for item in msglist:
            info = {}
            m = item.split(LINEEND)
            for i in m:
                m1 = i.split(':')
                if len(m1) == 2:
                    for a in attrs:
                        if m1[0].find(a) > -1:
                            info[a] = m1[1]
            infolist.append(info)
        return infolist

    def printMsg(self,msg):
        global attrs, START, END, LINEEND
        l = self.parseMsg(msg)
        infos = self.parseInfo(l)
        index = 1
        for i in infos:
            print "********the %dst message start**********"%index
            myPrint("********the %dst message start**********"%index)
            for a in attrs:
                if i.has_key(a):
                    print "%s:%s"%(a,i[a])
                    myPrint("%s:%s"%(a,i[a]))
            print "********the %dst message end************"%index
            myPrint("********the %dst message end************"%index)
            print 
            print
            index += 1
            
    def printDictMsg(self,dictMsg):
        index = 1
        for i in dictMsg:
            print "********the %dst message start**********"%index
            myPrint("********the %dst message start**********"%index)
            for a in attrs:
                print "%s:%s"%(a,i[a])
                myPrint("%s:%s"%(a,i[a]))
            print "********the %dst message end************"%index
            myPrint("********the %dst message end************"%index)
            print 
            print
            index += 1
        
    def parseToDict(self,msg):
        return self.parseInfo(self.parseMsg(msg))
    
    
    def ConstructMsg(self, adics):
        msg = START
        for a in attrs:
            if adics.has_key(a):
                msg += a + ':' + adics[a] + LINEEND
        msg += END
        return msg