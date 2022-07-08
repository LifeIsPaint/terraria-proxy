from hashlib import new
from operator import ne
from random import random
import socket
import time
import codecs
from threading import Thread
from tracemalloc import start
pServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 7777 + round(random() * 100)

pServer.bind((IP, PORT))
pServer.listen(5)


print('Server is now running on port', PORT)


def waiting ():
    # Terraria client
    (client, clientAddr) = pServer.accept()

    # Proxy Client
    pClient.connect(("127.0.0.1", 7777))

    t = Thread(target=startRecv, args=(client, pClient,True, ))
    t.start()

    t2 = Thread(target=startRecv, args=(pClient, client, False,))
    t2.start()

    print(clientAddr, 'connected.')
    waiting()

t = Thread(target=waiting)
t.start()

def sendToServer (buffer, socket: socket.socket):
    socket.send(buffer)

def editPacket (oldPacket):
    newPacket = ""
    newMessage = "Hello World!"

    newPacket += chr(1 + 8 + 1 + len(newMessage))
    
    for i in range(8):
        newPacket += chr(oldPacket[i+1])

    newPacket += chr(len(newMessage))

    newPacket += newMessage
    print(newPacket.encode('ascii').hex(' '))
    return newPacket.encode('ascii')

def sendMessagePacket (msg):
    newPacket = ""
    newMessage = msg

    newPacket += chr(1 + 8 + 1 + len(newMessage))
    msgType = bytes.fromhex("00 52 01 00 03 53 61 79")

    newPacket += "".join(map(chr, msgType))

    newPacket += chr(len(newMessage))

    newPacket += newMessage
    print(newPacket.encode('ascii').hex(' '))
    pClient.send(newPacket.encode('ascii'))


def startRecv(client: socket.socket, redirectClient: socket.socket, log):
    try:
        buffer = client.recv(1024)
        if(len(buffer) > 0):
            host, port = client.getpeername()
            if(log):
                bufferHex = buffer.hex(' ')
                bufferString = "".join(map(chr, buffer))
                # Filter for packets
                #if(bufferString.find('Say') != -1):
                #    print(bufferString)
                #    print(bufferHex)
                #    buffer = editPacket(buffer)
            sendToServer(buffer, redirectClient)
            startRecv(client, redirectClient, log)
        else:
            print(client.getpeername(), 'disconnected.')

    except Exception as e: 
        print(e)
        print(client.getpeername(), 'disconnected.')


while True:
    msg = input()
    sendMessagePacket(msg)
    
print('Press any key to continue...')
input()
