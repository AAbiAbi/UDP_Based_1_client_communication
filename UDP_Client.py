import socket
import sys
# from global_var import *
# Define constants
# =============
START_PACKET = 0xFFFF
# start of packet identifier
# global END_PACKET
END_PACKET = 0xFFFF
# end of packet identifier
# ========================Packet Types==============
DATA_PACKET = 0xFFF1
# DATA
ACK_PACKET = 0xFFF2
# ACK
REJECT_PACKET = 0xFFF3
# REJECT
# =================Reject sub codes===================
REJECT_SEQ = 0xFFF4
# out of sequence
REJECT_LEN = 0xFFF5
# length mismatch
REJECT_EOP = 0xFFF6
# end of packet missing
REJECT_DUP = 0xFFF7
# duplicate packet
# ================primitive================
client_id = 0x01  # Change to actual client ID
# maximum 0FF
# global ack_timer
ACK_TIMER = 3
ack_timer = 3  # seconds
# global MAX_RETRY
MAX_RETRY = 3

SERVER_IP = "127.0.0.1"# Server IP
SERVER_Port = 20001# Server Port
SERVER_ADDRESS = (SERVER_IP,SERVER_Port)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


bufferSize = 1024

def send_to_server(seg_No,packets):
    #input senNo and hashmanp packets
    str = packets.get(seg_No)
    if(str != None):
        print("MESSAGE:")
        print(" PAYLOAD:%s" % str, end="\n")
        print(" Client ID:%d" % client_id, end="\n")
        print(" Segment number:%d" % seg_No, end="\n")
        bytesToSend = str.encode()
        length_of_message = len(bytesToSend)
    # len of payload
        packet_len = length_of_message + 9
        DATA_PACKET_1 = DATA_PACKET >> 8
        DATA_PACKET_2 = DATA_PACKET & 0xFF
    # cut the DATA_PACKET in to two pieces.
        data_packet = bytearray(
            [START_PACKET >> 8, START_PACKET & 0xFF, client_id, DATA_PACKET_1, DATA_PACKET_2, seg_No, packet_len])
        data_packet.extend(bytesToSend)
        data_packet.extend([END_PACKET >> 8, END_PACKET & 0xFF])
        msgFromServer = None
        UDPClientSocket.sendto(data_packet,SERVER_ADDRESS)
        UDPClientSocket.settimeout(3)
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            # message = msgFromServer[0]
            # print(message[5])
            res_handling(msgFromServer, packets)
        except TimeoutError:  # fail after 1 second of no activity
            print("[ERROR:Time Expired] Resend again.\n")
            global MAX_RETRY
            if (MAX_RETRY > 1):
                MAX_RETRY = MAX_RETRY - 1
                send_to_server(seg_No, packets)
            else:
                print("Server does not respond.Stop Sending\n" )
                # stop_thread = True
                # return
                sys.exit()
                UDPClientSocket.close()
    else:
        pass


# ==================================================
def res_handling(bytesAddressPair,packets):
    message = bytesAddressPair[0]
    return_add = bytesAddressPair[1]
    client_id = message[2]


    # payload = message[7:len(message) - 2]
    if(len(message) == 8 and message[3] == 0xFF and message[4] == 0xF2):
        #receive ack from server
        seg_No = message[5]
        # print(seg_No)
        ACK_handler(seg_No,packets)
    elif (len(message) == 10 and message[3] == 0xFF and message[4] == 0xF3):
        seg_No = message[7]
        print("[REJECT]",end="")
        if(message[6] == 0xF4):
            print("(TYPE: Out of Sequence)")
        elif(message[6] == 0xF5):
            print("(TYPE: Length Mismatch)")
        elif (message[6] == 0xF6):
            print("(TYPE: End of packets Missing)")
        elif (message[6] == 0xF7):
            print("(TYPE: Duplicate packet)")
            return
        reject_handler(seg_No,packets)

def ACK_handler(seg_no,packets):
    if (packets.get(seg_no) != None):
        # if seg_No has been received from ACK, move the seg_No from the seg_set
        # seg_set.remove(seg_no)
        packets.pop(seg_no)
        # reset the timer and retry
        global MAX_RETRY
        MAX_RETRY = 3
        print("[RECEIVE ACK]")
        print("----------------------------------------------------------------")

        if(len(packets) == 0):
            print("--------------------------------")
            print("[FULLY REVEIVED]")
            print("--------------------------------")

            pass
    else:
        print("[Duplicate ACK received] DROP" )
        # pass
#======================================
def reject_handler(seg_no, packets):
    global MAX_RETRY
    if(MAX_RETRY > 1 ):
        MAX_RETRY = MAX_RETRY - 1
        print("....")
        send_to_server(seg_no, packets)
    else:
        print("[Cannot send]")
        print("-------------------------------------------------")
        return

#=================================================
def trigger_UDP_client(seg_No,packets):
    global MAX_RETRY
    MAX_RETRY = 3
    print("------------------------CLIENT MESSAGE--------------------------")
    send_to_server(seg_No, packets)


def trigger_rej_client(seg_No,packets,rej_type):
    print("--------------CLIENT MESSAGE------------")
    global MAX_RETRY
    MAX_RETRY = 3
    send_wrongmessage_to_server(seg_No,packets,rej_type)
#


#
#
def send_wrongmessage_to_server(seg_No,packets,rej_type):
    # input senNo and hashmanp packets
    change_END_PACKET(0xFFFF)
    str = packets.get(seg_No)
    print("MESSAGE:")
    if (str != None):
        print(" PAYLOAD:%s" % str, end="\n")
        print(" Client ID:%d" % client_id, end="\n")
        print(" Segment number:%d" % seg_No, end="\n")

        bytesToSend = str.encode()
        length_of_message = len(bytesToSend)
        packet_len = length_of_message + 9
        DATA_PACKET_1 = DATA_PACKET >> 8
        DATA_PACKET_2 = DATA_PACKET & 0xFF
        if(rej_type == 2):
            packet_len = 1
        elif(rej_type == 3):
            # global END_PACKET
            change_END_PACKET(0x0001)
            # END_PACKET = 0x0001
        elif(rej_type == 4):
            # global END_PACKET
            change_END_PACKET(0xFFFF)
            # END_PACKET = 0xFFFF
            data_packet = bytearray(

                [START_PACKET >> 8, START_PACKET & 0xFF, client_id, DATA_PACKET_1, DATA_PACKET_2, seg_No, packet_len])
            data_packet.extend(bytesToSend)
            data_packet.extend([END_PACKET >> 8, END_PACKET & 0xFF])
            msgFromServer = None

            UDPClientSocket.sendto(data_packet, SERVER_ADDRESS)
            # UDPClientSocket.sendto(data_packet, SERVER_ADDRESS)
            UDPClientSocket.settimeout(3)
            try:
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                res_handling(msgFromServer, packets)
            except TimeoutError:  # fail after 1 second of no activity
                print("[ERROR:Time Expired] Resend again.\n")
                global MAX_RETRY
                if (MAX_RETRY > 1):
                    MAX_RETRY = MAX_RETRY - 1
                    send_to_server(seg_No, packets)
                else:
                    print("Server dose not respond: %d" % seg_No)
                    UDPClientSocket.close()
            finally:
                # global END_PACKET
                change_END_PACKET(0xFFFF)
        else:
            print("wrong rej num")

        data_packet = bytearray(
            [START_PACKET >> 8, START_PACKET & 0xFF, client_id, DATA_PACKET_1, DATA_PACKET_2, seg_No, packet_len])
        data_packet.extend(bytesToSend)

        data_packet.extend([END_PACKET >> 8, END_PACKET & 0xFF])
        msgFromServer = None

        UDPClientSocket.sendto(data_packet, SERVER_ADDRESS)
        UDPClientSocket.settimeout(3)
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            res_handling(msgFromServer, packets)
        except TimeoutError:  # fail after 1 second of no activity
            print("[ERROR:Time Expired] Resend again.\n")
            # global retry
            if (MAX_RETRY > 1):
                MAX_RETRY = MAX_RETRY - 1
                send_to_server(seg_No, packets)
            else:
                # retry == 0
                print("Server does not respond.Stop Sending\n")
                UDPClientSocket.close()
    else:
        pass



def change_END_PACKET(content):
    global END_PACKET
    END_PACKET = content




if __name__ == '__main__':
    # i = 1
    # packets = {
    #     1: "da",
    #     2: "3edewddc",
    #     3: "jbdjiskzb",
    #     4: "nsjibhdiuj",
    #     5: "sdnjskan"
    # }
    # while(i <= 5):
    #     trigger_UDP_client(i, packets)
    #     i = i + 1

##comment the part, otherwise.....
    packet = {
        1: "1",
        2: "2",
        3: "jbdjiskzb",
        4: "nsjibhdiuj",
        5: "5",
        6:"h"

    }
    trigger_UDP_client(1,packet)
    trigger_UDP_client(3, packet)#out of sequence
    trigger_rej_client(2,packet,2) #length mismatch
    trigger_rej_client(3, packet, 3)#end of packets missing
    trigger_rej_client(3, packet, 4)#duplicate