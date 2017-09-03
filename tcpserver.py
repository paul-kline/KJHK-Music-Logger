from socket import *      #import the socket library

import KJHKMusicLogger as mlog
import emailSender as es
import sys
import time as tm 
import traceback as tb
import eventlet.timeout as evlet
import subprocess
def handleBurst(serv):
    recips =["technologyassist@kjhk.org","it@kjhk.org"]
    connfailures = 0
    emailMeAtMost = 60* 10 # 10 min in seconds
    lastEmailTime = 0
    while True:
        timeout = evlet.Timeout(30)
        try:
            print("bout to say accept..")            
            (conn,addr) = serv.accept()
            timeout.cancel();
            print("connection accepted")
            dat = conn.recv(BUFSIZE).decode('UTF-8', 'ignore')
            print("data received!!!")
            dat = dat.encode('cp850', errors='replace').decode('cp850').encode("utf-8", errors='replace').decode("utf-8")
            connfailures = 0
        except Timeout as t:
                sub = "Potential DS failure"
                bod = "The following timeout error was thrown:\n" + str(t)
                bod += "\nI am attempting to restart the device server."
                filepath ="C:/Users/WOAFR/Desktop/KJHK_SCRIPTS/restartDeviceServer.bat"
                p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
                stdout, stderr = p.communicate()
                print(p.returncode)
                es.sendEmail(recips,sub,bod)
        except KeyboardInterrupt:
            print("You have entered a keyboard interrupt. exiting.")
            conn.close()
            sys.exit(0)
            quit()
        except:
            connfailures += 1 
            mydelay = 30 #seconds
            e0 =str(sys.exc_info()[0])
            v0 = str(sys.exc_info()[1])
            t0 = str(tb.extract_tb(sys.exc_info()[2]))
            error0 = "ERROR:\n" + e0 + "\n\nVALUE:\n" + v0 + "\n\nTRACEBACK:\n" + t0 
            sub ="Connection to Device Server Error"
            bod="Error: \n" + error0
            
            try:
                conn.close()
                print("Connection closed!")
                connectionStatus = "successfully closed connection"
            except:
                connectionStatus = "failed to close connection:\n"
                connectionStatus+= str(sys.exc_info()[0])
                connectionStatus+= "\n" + str(sys.exc_info()[1])

            bod += "\n\n" + connectionStatus
            bod += "\n conn failures since last success: " + str(connfailures)
            bod += "\n Attempt reconnect in: " + str(mydelay) + " seconds."
            global tm
            if ((tm.time() - lastEmailTime) > emailMeAtMost):
                es.sendEmail(recips,sub,bod)
                lastEmailTime = tm.time()
            tm.sleep(mydelay)
            continue
        
        finally:
            timeout.cancel();

        try:
            print(dat)
        except:
            
            e =str(sys.exc_info()[0])
            v = str(sys.exc_info()[1])
            t = str(tb.extract_tb(sys.exc_info()[2]))
            error1 = "ERROR:\n" + e + "\n\nVALUE:\n" + v + "\n\nTRACEBACK:\n" + t 
            print("calling music logger..")
            try:
                mlog.handleDataBurst(dat)
            except:
                sub="Failed to print and failed to log"
                e2 =str(sys.exc_info()[0])
                v2 = str(sys.exc_info()[1])
                t2 = str(tb.extract_tb(sys.exc_info()[2]))
                error2 = "ERROR:\n" + e2 + "\n\nVALUE:\n" + v2 + "\n\nTRACEBACK:\n" + t2
                bod="print error:\n" + error1 + "\n" + "log error:\n" + error2
                es.sendEmail(recips,sub,bod)
            else:
                print("used to be email codehere")
                # if we s succeeded in logging, but there was a print error
                #sub ="Error printing but logging song raised no exceptions"
                #bod="print error: \n" + error1
                #bod += "\n dat=\n" + dat
                #es.sendEmail(recips,sub,bod)
        else:
            try:
                mlog.handleDataBurst(dat)
            except:
                sub="success printing, but logging threw an exception"
                e3 =str(sys.exc_info()[0])
                v3 = str(sys.exc_info()[1])
                t3 = str(tb.extract_tb(sys.exc_info()[2]))
                error3 = "ERROR:\n" + e3 + "\n\nVALUE:\n" + v3 + "\n\nTRACEBACK:\n" + t3 
                bod="dat=\n" + dat +"\n\n Error logging:\n" + error3
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


