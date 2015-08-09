##client.py
from socket import *

HOST = 'localhost'
PORT = 55555    #our port from before
ADDR = (HOST,PORT)
BUFSIZE = 4096



def mysend(str):
    cli = socket( AF_INET,SOCK_STREAM)
    cli.connect((ADDR))
    cli.send(bytes(str,'utf-8'))
    
