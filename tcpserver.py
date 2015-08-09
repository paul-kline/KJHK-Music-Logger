from socket import *      #import the socket library

import KJHKMusicLogger as mlog

def handleBurst(serv):
    while True:
        print("bout to say accept..")
        (conn,addr) = serv.accept()
        print("connection accepted")
        dat = conn.recv(BUFSIZE).decode('UTF-8')
        print("data received!!!")
        print(dat)
        print("calling music logger..")
        mlog.handleDataBurst(dat)
        
        conn.close()
        print("Connection closed!")
    
##let's set up some constants
HOST = ''    #TODO change to itty bitty wideorbit only IP
PORT = 55555    #Device Server output port
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 8192    #this is probably much larger than neccessary. 

## now we create a new socket object (serv)

serv = socket( AF_INET,SOCK_STREAM)    

##bind our socket to the address
serv.bind((ADDR))    #the double parens are to create a tuple with one element
serv.listen(5)    #5 is the maximum number of queued connections we'll allow
print("listening..")
handleBurst(serv)


