import socket
import select

# Array of admins
admins = ["admin1", "admin2"]

# Dictionary to store client sockets and usernames
clients = {}

# Dictionary to store muted users
muted_users = {}

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server socket to a specific address and port
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(10)

# Add the server socket to the list of readable sockets
sockets_list = [server_socket]

print("Server started on {}:{}".format(server_address[0], server_address[1]))

def receive_message(client_socket):
    try:
        # Receive message from the client
        message = client_socket.recv(4096).decode('utf-8')

        if message:
            return message.strip()
        else:
            # If no data received, remove the client socket
            remove_client(client_socket)

    except Exception as e:
        # Error occurred, remove the client socket
        remove_client(client_socket)


def remove_client(client_socket):
    # Remove the client socket from the list of sockets
    sockets_list.remove(client_socket)

    # Close the client socket
    client_socket.close()

    # Get the username of the client
    username = clients[client_socket]

    # Remove the client from the clients dictionary
    del clients[client_socket]

    # Broadcast the user left message to other clients
    broadcast_message("@server", "{} has left the chat!".format(username))

def broadcast_message(sender, message):
    # Iterate over all connected clients and send the message
    for client_socket in clients:
        if client_socket != server_socket:
            client_socket.send("{}: {}".format(sender, message).encode('utf-8'))

while True:
    # Use select to multiplex inputs from server socket and client sockets
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # New client connection received
            client_socket, client_address = server_socket.accept()

            # Receive the username from the client
            username = receive_message(client_socket)

            if username:
                # Add the client socket and username to the dictionaries
                clients[client_socket] = username

                # Add the client socket to the list of sockets
                sockets_list.append(client_socket)

                # Send a welcome message to the client
                client_socket.send("Welcome to the chat!".encode('utf-8'))

                # Broadcast the user joined message to other clients
                broadcast_message("@server", "{} has joined the chat!".format(username))

        else:
            # Receive and process message from an existing client
            message = receive_message(notified_socket)
            print(message)

            if message:
                # Get the username of the client
                username = clients[notified_socket]

                # Check if the user is an admin
                is_admin = username in admins

                # Process the message based on the command number
                # command_number = int(message[message.index(username) + len(username)])
                command_number = int(message[message.index(username) + len(username) + 1])
                print(command_number)
                if command_number == 1:
                    # Chat message
                    count = int(message[message.index(username) + len(username) + 2 : message.index(username) + len(username) + 4])
                    chat_message = message[message.index(username) + len(username) + 4 : message.index(username) + len(username) + 4 + count]
                    # Implement chat message logic here
                elif command_number == 2 and is_admin:
                    # Admin permissions to another user
                    count = int(message[message.index(username) + len(username) + 2 : message.index(username) + len(username) + 4])
                    user_to_give_permissions = message[message.index(username) + len(username) + 4 : message.index(username) + len(username) + 4 + count]
                    # Implement admin permissions logic here
                elif command_number == 3 and is_admin:
                    # Kick another user
                    count = int(message[message.index(username) + len(username) + 2 : message.index(username) + len(username) + 4])
                    user_to_kick = message[message.index(username) + len(username) + 4 : message.index(username) + len(username) + 4 + count]
                    # Implement kick logic here
                elif command_number == 4 and is_admin:
                    # Mute another user
                    count = int(message[message.index(username) + len(username) + 2 : message.index(username) + len(username) + 4])
                    user_to_mute = message[message.index(username) + len(username) + 4 : message.index(username) + len(username) + 4 + count]
                    # Implement mute logic here
                elif command_number == 5 and is_admin:
                    # Private chat between users
                    count1 = int(message[message.index(username) + len(username) + 2 : message.index(username) + len(username) + 4])
                    private_username = message[message.index(username) + len(username) + 4 : message.index(username) + len(username) + 4 + count1]
                    count2 = int(message[message.index(private_username) + len(private_username) + 2 : message.index(private_username) + len(private_username) + 4])
                    private_message = message[message.index(private_username) + len(private_username) + 4 : message.index(private_username) + len(private_username) + 4 + count2]
                    # Implement private chat logic here

    for notified_socket in exception_sockets:
        # Handle exception by removing the socket
        remove_client(notified_socket)
