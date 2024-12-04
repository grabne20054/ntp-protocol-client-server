import socket
import time


def ntp_client(server_host="127.0.0.1", server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        t1 = time.time()  # Time when the request is sent
        client_socket.sendto(b"TIME_REQUEST", (server_host, server_port))

        data, _ = client_socket.recvfrom(1024)
        t4 = time.time()  # Time when the response is received

        # Parse t2 and t3 from the server's response
        t2, t3 = map(float, data.decode().split(","))

        # Calculate RTT and offset
        rtt = t4 - t1
        offset = ((t2 - t1) + (t3 - t4)) / 2
        adjusted_time = t4 + offset

        print(f"Server Time (t2): {t2}")
        print(f"Server Response Time (t3): {t3}")
        print(f"Round Trip Time (RTT): {rtt:.6f} seconds")
        print(f"Time Offset: {offset:.6f} seconds")
        print(f"Adjusted Client Time: {time.ctime(adjusted_time)}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    ntp_client()
