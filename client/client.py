import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import socket
import time
from server import NTP



def ntp_client(server_host="127.0.0.1", server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = NTP.NTPPacket()

    try:
        t1 = time.time() 
        packet.set_t1(t1)
        print(f"Requesting time from {server_host}:{server_port}")
        # send packet 
        client_socket.sendto(packet.to_binary(), (server_host, server_port))
        print("Sent request")

        data, _ = client_socket.recvfrom(1024)
        t4 = time.time()  # Time when the response is received
        packet = NTP.NTPPacket.from_binary(data)
        packet.set_t4(t4)

        # set local time
        local_time = packet.synchronize()
        local_time = time.strftime("%H:%M:%S", time.localtime(local_time))
        print(f"Synchronized Time: {local_time}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    ntp_client()
