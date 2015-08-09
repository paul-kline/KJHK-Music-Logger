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
HOST = ''    #we are the host
PORT = 55555    #arbitrary port not currently in use
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 4096    #reasonably sized buffer for data

## now we create a new socket object (serv)
## see the python docs for more information on the socket types/flags
serv = socket( AF_INET,SOCK_STREAM)    

##bind our socket to the address
serv.bind((ADDR))    #the double parens are to create a tuple with one element
serv.listen(5)    #5 is the maximum number of queued connections we'll allow
print("listening..")
handleBurst(serv)


