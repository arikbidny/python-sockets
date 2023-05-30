import socket
import select

# Replace 'localhost' with the server's IP address or hostname
server_host = 'localhost'
server_port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Function to receive messages from the server


def receive_messages():
    while True:
        try:
            # Use select to monitor socket for read events
            read_sockets, _, _ = select.select([client_socket], [], [])

            for sock in read_sockets:
                message = sock.recv(4096).decode()
                print(message)
        except:
            # If there is an error receiving the message, assume the server is disconnected
            client_socket.close()
            break

# Function to send messages to the server


def send_message():
    while True:
        try:
            # Use select to monitor stdin for input events
            _, write_sockets, _ = select.select([], [client_socket], [])

            for sock in write_sockets:
                message = input()
                client_socket.send(message.encode())
        except:
            # If there is an error sending the message, assume the server is disconnected
            client_socket.close()
            break


receive_messages()
send_message()
