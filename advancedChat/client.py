import socket
import select
import msvcrt

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 8888)
client_socket.connect(server_address)

# Get the username from the user
username = input("Enter your username: ")
client_socket.send(username.encode('utf-8'))

# Function to receive messages from the server
def receive_message():
    try:
        message = client_socket.recv(4096).decode('utf-8')
        if message:
            print(message)
    except socket.error:
        # Error occurred, connection closed by server
        print("Connection closed by server.")
        client_socket.close()
        exit()

while True:
    # Use select to multiplex inputs from keyboard and server socket
    read_sockets, _, _ = select.select([client_socket,], [], [], 0.1)

    for sock in read_sockets:
        if sock == client_socket:
            # Server sent a message, receive and display it
            receive_message()

    if msvcrt.kbhit():
        # Get user input from the keyboard
        message = msvcrt.getche().decode('utf-8')

        # Check if the user wants to quit
        if message.lower() == 'quit':
            client_socket.send(message.encode('utf-8'))
            break

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))

# Close the client socket
client_socket.close()
