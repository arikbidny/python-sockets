import socket
import select
import msvcrt


# Get the username from the user
username = input("Enter your username: ")

# Connect to the server
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    # Receive username input from the user
    client_socket.send(username.encode())

    return client_socket


# Send chat message to the server
def send_chat_message(client_socket, message):
    client_socket.send(message.encode())


def start_client(client_socket):
    while True:
        # Check if there is an input from the user
        if msvcrt.kbhit():
            message = input("message: ")
            print(message)
            
            send_chat_message(client_socket, message)
            
        # Check if there is incoming data from the server
        if client_socket in select.select([client_socket], [], [], 0)[0]:
          data = client_socket.recv(1024).decode()
          print(data)   
            
client_socket = connect_to_server()
start_client(client_socket)
            