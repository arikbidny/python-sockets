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
    # username_length = len(username)
    # command = 1
    # message_length = len(message)
    # data = f"{username_length}{username}{command}{message_length:02d}{message}"
    client_socket.send(message.encode())

# Give admin permissions to another user
def give_admin_permissions(client_socket, user):
    username_length = len(username)
    command = 2
    message_length = len(user)
    data = f"{username_length}{username}{command}{message_length:02d}{user}"
    client_socket.send(data.encode())

# Kick another user from the chat
def kick_user(client_socket, user):
    username_length = len(username)
    command = 3
    message_length = len(user)
    data = f"{username_length}{username}{command}{message_length:02d}{user}"
    client_socket.send(data.encode())

# Mute another user
def mute_user(client_socket, user):
    username_length = len(username)
    command = 4
    message_length = len(user)
    data = f"{username_length}{username}{command}{message_length:02d}{user}"
    client_socket.send(data.encode())

# Send a private message to another user
def send_private_message(client_socket, recipient, message):
    username_length = len(username)
    command = 5
    recipient_length = len(recipient)
    message_length = len(message)
    data = f"{username_length}{username}{command}{message_length:02d}{recipient_length}{recipient}{message}"
    client_socket.send(data.encode())

# Start the client
def start_client(client_socket):
    while True:
        # Check if there is input from the user
        if msvcrt.kbhit():
            message = input("message: ")
            print(message)
            
            username_length = int(message[0]);
            print(username_length)
            
            
            username_name = message[1:username_length+1]
            
            print(username_name)

            if message == "quit":
                break

            send_chat_message(client_socket, message)

        # Check if there is incoming data from the server
        if client_socket in select.select([client_socket], [], [], 0)[0]:
            data = client_socket.recv(1024).decode()
            
            if not data:
                # Server closed the connection
                break

            # Process and display the received data
            print(data)

    client_socket.close()
    
client_socket = connect_to_server()
start_client(client_socket)
