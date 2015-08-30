import re

START = "$START$"
END = "$END$"
LINEEND = "$$$"
attrs = ['name','isDead','growth','pos','type','port']
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
            for a in attrs:
                if i.has_key(a):
                    print "%s:%s"%(a,i[a])
            print "********the %dst message end************"%index
            print 
            print
            index += 1
            
    def printDictMsg(self,dictMsg):
        index = 1
        for i in dictMsg:
            print "********the %dst message start**********"%index
            for a in attrs:
                print "%s:%s"%(a,i[a])
            print "********the %dst message end************"%index
            print 
            print
            index += 1
        
    def parseToDict(self,msg):
        return self.parseInfo(self.parseMsg(msg))