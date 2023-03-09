from UDP_Client import *
from UDP_Server import *
import threading
import collections

server_IP = "127.0.0.1"# Server IP
server_Port = 20001# Server Port
server_address = (server_IP,server_Port)
# bufferSize = 1024# need to be changed
# seg_hashset = set() #
# Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# print(1)
# ===================procedure 1  ==========================
def procesdure1():
    i = 1
    packets = {
        1: "da",
        2: "3edewddc",
        3: "jbdjiskzb",
        4: "nsjibhdiuj",
        5: "sdnjskan"
    }
    while(i <= 5):
        trigger_UDP_client(i, packets)
        i = i + 1

# trigger_UDP_server(server_address)
# trigger_UDP_client(1,packets)
##proceduce
###The client sends five packets (Packet 1, 2, 3, 4, 5) to the server.
##The server acknowledges with ACK receive of each correct packet from client by sending five ACKs, one ACK for each 5 received packets.
if __name__ == '__main__':
    try:
       # thread.start_new_thread( trigger_UDP_server() )
       t1 = threading.Thread(target=trigger_UDP_server, args=(),name='ServerThread')
       t2 = threading.Thread(target=procesdure1, args=(), name='ClientThread1')

       t1.start()
       t2.start()

    except:
       print("Error: unable to start thread")
    finally:
        print("=======================procedure1=============c")


# ======================procedure 2=====================
'''
The client then sends another five packets (Packet 1, 2, 3, 4, 5) to the server, emulating one correct packet and four packets with errors.
The server acknowledges with ACK receive of correct packet from client, and with corresponding Reject sub codes for packets with errors. 

'''
# server_IP_2 = "127.0.0.1"# Server IP
# server_Port_2 = 20002# Server Port
# server_address_2 = (server_IP_2,server_Port_2)
print("             ")

# try:
#    # thread.start_new_thread( trigger_UDP_server() )
#    # t1 = threading.Thread(target=trigger_UDP_server, args=(server_address_2,),name='ServerThread')
#    # t21 = threading.Thread(target=trigger_UDP_client, args=(1,packets,), name='ClientThread1')
#    t31 = threading.Thread(target= send_wrongmessage_to_server, args=(2, packets,1, ), name='ClientThread2')
#    t41 = threading.Thread(target= send_wrongmessage_to_server, args=(3, packets,2, ), name='ClientThread3')
#    t51 = threading.Thread(target= send_wrongmessage_to_server, args=(4, packets,3, ), name='ClientThread4')
#    t61 = threading.Thread(target= send_wrongmessage_to_server, args=(5, packets,4, ), name='ClientThread5')
#
#    # t1.start()
#    # t21.start()
#    t31.start()
#    t41.start()
#    t51.start()
#    t61.start()
#
#    # t1.join()
#    # t2.join()
#    # t3.join()
#    # t4.join()
#    # t5.join()
#    # t6.join()
# except:
#    print("Error: unable to start thread")
#
# # trigger_UDP_server(server_address)
# # trigger_UDP_client(1,packets)
# # trigger_UDP_client(4,packets)
# # trigger_UDP_client(2,packets)
# # trigger_UDP_client(3,packets)
# # trigger_UDP_client(5,packets)
# # # for key in packets:
# #     trigger_UDP_client(key,packets)
# #     print(2)
