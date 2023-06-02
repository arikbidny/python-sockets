import select
import socket

# List of admins
admins = ['admin1', 'admin2']

# Dictionary to store client sockets and usernames
clients = {}

# Dictionary to store muted users
muted_users = {}

# List to store private chats
private_chats = []

# Broadcast message to all connected clients
def broadcast(message):
    for client in clients.values():
        client.send(message.encode())

# Send message to a specific client
def send_message(client, message):
    client.send(message.encode())

# Process the chat message
def process_chat_message(username, message):
    timestamp = "08:02"  # Replace with appropriate timestamp logic
    full_message = f"{timestamp} {username}: {message}"
    broadcast(full_message)

# Process admin permissions command
def process_admin_permissions(admin, user):
    if admin in admins:
        admins.append(user)
        broadcast(f"09:45 {user} has been granted admin permissions!")

# Process kick user command
def process_kick_user(admin, user):
    if admin in admins and user in clients:
        clients[user].send("You have been kicked from the chat!")
        clients[user].close()
        del clients[user]
        broadcast(f"09:45 {user} has been kicked from the chat!")

# Process mute user command
def process_mute_user(admin, user):
    if admin in admins and user in clients:
        muted_users[user] = True
        send_message(clients[user], "You cannot speak here")

# Process private message command
def process_private_message(sender, recipient, message):
    if sender in clients and recipient in clients:
        private_message = f"Private message from {sender}: {message}"
        send_message(clients[recipient], private_message)

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    # Add the server socket to the list of readable connections
    sockets_list = [server_socket]

    print("Chat server started on localhost:12345")

    while True:
        # Get the list of sockets that are ready to be read
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()

                # Receive username from client
                username = client_socket.recv(1024).decode().strip()

                # Store the client socket and username
                clients[username] = client_socket

                print(f"New client connected: {username}")

                # Broadcast user join message
                broadcast(f"{username} has joined the chat!")

            # Incoming message from a client
            else:
                try:
                    data = sock.recv(1024).decode().strip()

                    # Disconnect if client closed the connection
                    if not data:
                        disconnected_user = next(
                            key for key, value in clients.items() if value == sock
                        )
                        sock.close()
                        del clients[disconnected_user]
                        broadcast(f"09:45 {disconnected_user} has left the chat!")
                        continue

                    # Extract username, command, and message from the data
                    username_length = int(data[0])
                    username = data[1:1+username_length]
                    command = int(data[1+username_length])
                    message_length = int(data[2+username_length:4+username_length])
                    message = data[4+username_length:4+username_length+message_length]

                    # Process different commands
                    if command == 1:
                        process_chat_message(username, message)
                    elif command == 2:
                        process_admin_permissions(username, message)
                    elif command == 3:
                        process_kick_user(username, message)
                    elif command == 4:
                        process_mute_user(username, message)
                    elif command == 5:
                        recipient_length = int(data[4+username_length+message_length])
                        recipient = data[5+username_length+message_length:5+username_length+message_length+recipient_length]
                        private_message = data[5+username_length+message_length+recipient_length:]
                        process_private_message(username, recipient, private_message)

                except Exception as e:
                    print(f"Error: {e}")

        server_socket.close()

start_server()
