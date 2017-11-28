import socket


ack = "ACK"
sentAck = "koko,0,ACK"
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("the server is ready  ")
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
    if arr[2] == "ACK" and int(arr[1]) == seqSnd:
        return 1
    else:
        return 0


def verifySeq(packet):
    global seqRcvd
    packet = packet.decode("UTF-8")
    arr = packet.split(",")
    if int(arr[1])== seqRcvd:
        return 1
    else:
        return 0


def receive():
    global sentAck
    global seqRcvd
    data, clientAddress = serverSocket.recvfrom(2048)
    print("packet received: " + data.decode("UTF-8"))
    if (verifyCheckSum(data) and verifySeq(data)):
        sentAck = createPacket(ack, seqRcvd)
        print("ACK Packet to send : " + sentAck)
        serverSocket.sendto(sentAck.encode('UTF-8'), clientAddress)
        data = data.decode("UTF-8")
        arr = data.split(",")
        seqRcvd=1-seqRcvd
        return arr[2], clientAddress
    serverSocket.sendto(sentAck.encode('UTF-8'), clientAddress)
    return receive()


def sendPacket(packet, clientAddress):
    global seqSnd
    try:
        print("Packet to send as a response : " + packet)
        serverSocket.sendto(packet.encode('UTF-8'), clientAddress)
        ack = serverSocket.recv(2048)
        print("ACK received: " + ack.decode('UTF-8'))
        if not (verifyCheckSum(ack) and isACK(ack)):
            ack = serverSocket.recv(2048)
        else:
            seqSnd = 1 - seqSnd
    except socket.timeout:
        sendPacket(packet, clientAddress)


def getCheckSum(data):
    return "koko"


def createPacket(data, seq):
    checkSum = getCheckSum(data)
    packet = checkSum + ',' + str(seq) + ',' + str(data)
    return packet


while 1:
    k, clientAddress = receive()
    print("data from the packet : " + k)
    packet_to_send = createPacket(k.upper(), seqSnd)
    sendPacket(packet_to_send, clientAddress)
    print("---------------------------------")
