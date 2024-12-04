import socket
import time
import NTP


def ntp_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        message, client_address = server_socket.recvfrom(1024)
       
        print("Received request from", client_address)
        t2 = time.time()
        # Send back both t2 and t3 as part of the response
        packet = NTP.NTPPacket.from_binary(message)
        packet.set_t2(t2)

        
        t3 = time.time()  # Time when the response is sent
        packet.set_t3(t3)
        server_socket.sendto(packet.to_binary(), client_address)


if __name__ == "__main__":
    ntp_server()
