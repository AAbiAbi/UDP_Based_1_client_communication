from UDP_Client import *
from UDP_Server import *
import threading

server_IP = "127.0.0.1"# Server IP
server_Port = 20001# Server Port
server_address = (server_IP,server_Port)
# bufferSize = 1024# need to be changed
# seg_hashset = set() #
# Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# print(1)
# ===================procedure 1  ==========================
def procesdure2():
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

if __name__ == '__main__':

    try:
       # thread.start_new_thread( trigger_UDP_server() )
       t1 = threading.Thread(target=trigger_UDP_server, args=(),name='ServerThread')
       t2 = threading.Thread(target=procesdure2, args=(), name='ClientThread1')

       t1.start()
       t2.start()

    except:
       print("Error: unable to start thread")
    finally:
        print("")
        print("=======================procedure1=============")
