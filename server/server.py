import socket
import time


def ntp_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        t2 = time.time()  # Time when the request is processed
        # Send back both t2 and t3 as part of the response
        t3 = time.time()  # Time when the response is sent
        server_socket.sendto(f"{t2},{t3}".encode(), client_address)


if __name__ == "__main__":
    ntp_server()
