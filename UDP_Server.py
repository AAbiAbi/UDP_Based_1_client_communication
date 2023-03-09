import socket
import collections
# Define constants
SERVER_IP = "127.0.0.1"# Server IP
SERVER_Port = 20001# Server Port
SERVER_ADDRESS = (SERVER_IP,SERVER_Port)
START_PACKET = 0xFFFF
END_PACKET = 0xFFFF
DATA_PACKET = 0xFFF1
ACK_PACKET = 0xFFF2
REJECT_PACKET = 0xFFF3
REJECT_SEQ = 0xFFF4
REJECT_LEN = 0xFFF5
REJECT_EOP = 0xFFF6
REJECT_DUP = 0xFFF7
seg_hashset = set()
seg_deque = collections.deque()

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind(SERVER_ADDRESS)
# =================def===================
def send_reject1_back(address,client_id,seg_No):
    bytesToSend = bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, REJECT_PACKET >> 8, REJECT_PACKET & 0xFF, REJECT_SEQ >> 8,
         REJECT_SEQ & 0xFF, seg_No, END_PACKET >> 8,
         END_PACKET & 0xFF])
    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [REJECT(TYPE:Out of Sequence)]\n" )
    # print("==============================\n")

def send_reject2_back(address,client_id,seg_No):
    bytesToSend = bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, REJECT_PACKET >> 8, REJECT_PACKET & 0xFF, REJECT_LEN >> 8,
         REJECT_LEN & 0xFF, seg_No, END_PACKET >> 8,
         END_PACKET & 0xFF])
    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [REJECT(TYPE:Length Mismatch)]\n")
    # print("==============================\n")

def send_reject3_back(address,client_id,seg_No):
    bytesToSend = bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, REJECT_PACKET >> 8, REJECT_PACKET & 0xFF, REJECT_EOP >> 8,
         REJECT_EOP & 0xFF, seg_No, END_PACKET >> 8,
         END_PACKET & 0xFF])
    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [REJECT(TYPE:End of packet missing)]\n")
    # print("==============================\n")


def send_reject4_back(address,client_id,seg_No):
    bytesToSend = bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, REJECT_PACKET >> 8, REJECT_PACKET & 0xFF,REJECT_DUP >> 8, REJECT_DUP & 0xFF, seg_No, END_PACKET >> 8,
         END_PACKET & 0xFF])

    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [REJECT(TYPE:Duplicate packet)]\n")
    # print("==============================\n")


def send_ACK(address,client_id,seg_No):
    bytesToSend =  bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, ACK_PACKET >> 8, ACK_PACKET& 0xFF, seg_No, END_PACKET >> 8, END_PACKET & 0xFF])
    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [ACKNOWLEDGED]")
    # print("==============================\n")

def send_ACK_total(address,client_id,seg_No):
    bytesToSend = bytearray(
        [START_PACKET >> 8, START_PACKET & 0xFF, client_id, ACK_PACKET >> 8, ACK_PACKET & 0xFF, 6, END_PACKET >> 8,
         END_PACKET & 0xFF])
    UDPServerSocket.sendto(bytesToSend, address)
    print("||   [ACKNOWLEDGED FOR FIVE MESSAGES]\n")
    # print("==============================\n")


# ===================================

def trigger_UDP_server():
    bufferSize = 1024
    print("UDP server up and listening:\n")
    while True:
        if(getattr(UDPServerSocket, '_closed') == True):
            break
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    # msgFromServer = "ACK"
    # bytesToSend = str.encode(msgFromServer)
        message = bytesAddressPair[0]
        print("===================SERVER==================")
        return_add = bytesAddressPair[1]
        client_id = message[2]
        seg_No = message[5]
        payload = message[7:len(message) - 2]
        # print("==================\n")
        clientMsg = "||   Message:{}".format(payload.decode("utf-8"))
        # clientIP = "Client IP Address:{}".format(client_id)
        print(clientMsg, end="\n")
        print("||   Client ID:%d" % client_id, end="\n")
        print("||   Segment number:%d" % seg_No, end="\n")
        print("|| ")
        if (seg_No in seg_hashset ):
            send_reject4_back(return_add,client_id,seg_No)
            print("===========================================")
        elif (message[6] != len(message)):
            send_reject2_back(return_add,client_id,seg_No)
            print("===========================================")
        elif (message[len(message) - 2] != 0xFF or message[len(message) - 1] != 0xFF):
            send_reject3_back(return_add,client_id,seg_No)
            print("===========================================")
        elif (seg_No != len(seg_hashset) + 1):
            send_reject1_back(return_add,client_id,seg_No)
            print("===========================================")
        else:
        # Sending an ACK to client
        # global seg_hashset
            seg_hashset.add(seg_No)
            send_ACK(return_add, client_id, seg_No)
            print("===========================================")
            # if (len(seg_hashset) == 5):
            #
            #     send_ACK_total(return_add,client_id,seg_No)
            #     # global seg_hashset
            #     seg_hashset.clear()
            #     seg_No = 1
            #     print("Clear hashset \n")
            #     print("-------------SERVER FIN------------------")


# ================fin def==================

if __name__ == '__main__':
    trigger_UDP_server()
# Create a datagram socket
