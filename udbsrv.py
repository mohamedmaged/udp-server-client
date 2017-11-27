import socket
import select
from threading import Thread
ack = "ACK"
sentAck = "dummyack,kjk, 56"
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("the server is ready  ")
#k = receive()
serverSocket.settimeout(10)


seqSnd = 0
seqRcvd = 0


def verifyCheckSum(packet):
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if arr[0] == getCheckSum(arr[2]):
        return 1
    else:
        return 0


def isACK(packet):
    global seqSnd
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if arr[2] == "ACK" and arr[1] == seqSnd:
        return 1
    else:
        return 0


def verifySeq(packet):
    global seqRcvd
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if arr[1] == seqRcvd:
        return 1
    else:
        return 0


def receive():
    global sentAck
    global seqRcvd
    data, clientAddress = serverSocket.recvfrom(2048)
    if (verifyCheckSum(data) and verifySeq(data)):
        sentAck = createPacket(ack, seqRcvd)
        serverSocket.sendto(sentAck.encode('UTF-8'), clientAddress)
        data = data.decode("UTF-8")
        arr = data.split(",")
        seqRcvd=1-seqRcvd
        return arr[2], clientAddress
    serverSocket.sendto(sentAck.encode('UTF-8'), clientAddress)
    return receive()


def sendPacket(packet, clientAddress):
    global ack
    global seqSnd
    try:
        serverSocket.sendto(packet.encode('UTF-8'), clientAddress)
        ack = serverSocket.recv(2048)
        if not (verifyCheckSum(ack) and isACK(ack)):
            ack = serverSocket.recv(2048)
        else:
            seqSnd = 1 - seqSnd
    except socket.timeout:
        sendPacket(packet)


def getCheckSum(data):
    return "koko";


def createPacket(data, seq):
    checkSum = getCheckSum(data);
    packet = checkSum + ',' + str(seq) + ',' + data
    return packet;


while 1:
    k, clientAddress = receive()
    print(k)
    sendPacket(createPacket(k.upper(), seqSnd), clientAddress)
