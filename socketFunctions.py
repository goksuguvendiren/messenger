import socket
import sys
import threading

ListeningPort = 5555
SendingPort = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', ListeningPort))

def ListenTo():
    while True:
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]
        print "geldi : ", data

def SendTo():
    while True: 
        msg = raw_input('Enter message to send : \n')
     
        s.sendto(msg, ('', SendingPort))

ListeningThread = threading.Thread(name = 'LThread', target = ListenTo)
ListeningThread.start()
SendTo()