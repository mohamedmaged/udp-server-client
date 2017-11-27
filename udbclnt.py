import socket
import select
from threading import Thread

serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(0.2)
ack = "ACK"
sentAck = "dummyack,1,2"

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
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if arr[2] == "ACK" and arr[1] == seqSnd:
        return 1
    else:
        return 0


def verifySeq(packet):
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if arr[1] == seqSnd:
        return 1
    else:
        return 0


def receive():
    data, clientAddress = clientSocket.recvfrom(2048)
    if (verifyCheckSum(data) and verifySeq(data)):
        sentAck = createPacket(ack, seqRcvd)
        clientSocket.sendto(sentAck.encode('UTF-8'), (serverName, serverPort))
        data = data.decode("UTF-8")
        arr = data.split(",")
        seqRcvd=1-seqRcvd
        return arr[2]
    clientSocket.sendto(sentAck.encode('UTF-8'), (serverName, serverPort))
    return receive()


def sendPacket(packet):
    try:
        clientSocket.sendto(packet.encode('UTF-8'), (serverName, serverPort))
        ack = clientSocket.recv(2048)
        if not (verifyCheckSum(ack) and isACK(ack)):
            ack = clientSocket.recv(2048)
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
    k = input("enter any thing")
    sendPacket(createPacket(k.upper(), seqSnd))
    k = receive()
    print(k)
