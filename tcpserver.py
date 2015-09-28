from socket import *      #import the socket library

import KJHKMusicLogger as mlog
import emailSender as es
import sys

def handleBurst(serv):
    while True:
        print("bout to say accept..")
        (conn,addr) = serv.accept()
        print("connection accepted")
        dat = conn.recv(BUFSIZE).decode('UTF-8', 'ignore')
        print("data received!!!")
        dat = dat.encode('cp850', errors='replace').decode('cp850').encode("utf-8")
        try:
            print(dat)
        except:
            recips =["pauliankline@gmail.com","it@kjhk.org"]
            e=sys.exc_info()[0]
            print("calling music logger..")
            try:
                mlog.handleDataBurst(dat)
            except:
                sub="Failed to print and failed to log"
                e2=sys.exc_info()[0]
                bod="print error:\n" + e + "\n" + "log error:\n" + e2
                es.sendEmail(recips,sub,bod)
            else:
                # if we s succeeded in logging, but there was a print error
                sub ="Error printing but logging song raised no exceptions"
                bod="print error: \n" + e
                es.sendEmail(recips,sub,bod)
        else:
            try:
                mlog.handleDataBurst(dat)
            except:
                sub="success printing, but logging threw an exception"
                e3=sys.exc_info()[0]
                bod="dat=\n" + dat +"\n\n Error logging:\n" + e3
                es.sendEmail(recips,sub,bod)

        conn.close()
        print("Connection closed!")

##let's set up some constants
HOST = '' #empty because we are on localhost now
          #using DS-LOGGER '192.168.1.4'    #TODO change to itty bitty wideorbit only IP
PORT = 55555    #Device Server output port
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 8192    #this is probably much larger than neccessary.

## now we create a new socket object (serv)

serv = socket( AF_INET,SOCK_STREAM)

##bind our socket to the address
#serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serv.bind((ADDR))    #the double parens are to create a tuple with one element
serv.listen(5)    #5 is the maximum number of queued connections we'll allow
print("listening..")
handleBurst(serv)


