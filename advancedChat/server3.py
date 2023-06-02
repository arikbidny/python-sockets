import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"  # Local Host server


# def print_client_sockets(client_sockets):
#     for c in client_sockets:
#         print(c.getpeername())



print("Listening for clients...")
client_sockets = []
open_client_sockets = []
messages_to_send = []

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
        

def start_server():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    
    # Add the server socket to the list of readable connections
    sockets_list = [server_socket]
    
    print(f"Chat server started at {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        # Get the list of the sockets that are ready to be read
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                print("New connection")
                client_socket, client_address = server_socket.accept()
                
                # Receive username from client 
                username = client_socket.recv(1024).decode().strip()
                print(username);
                
                # Store the client socket and username
                clients[username] = client_socket
                
                print(clients)
                
                print(f"New client connected: {username}")
                
                # Broadcast user join message
                broadcast(f"{username} has joined the chat!")
            
            # Incoming message from a client
            else:
                print("Incoming message from a client")
                try:
                    data = sock.recv(1024).decode().strip()            
                    print(data)
                except Exception as e:
                    print(f"Error: {e}")
        
        server_socket.close()


start_server()

# # New Client -> Open a new socket connection
# # Existing Client -> Read the name and print to the command line
# while True:
#     rlist, wlist, xlist = select.select(
#         [server_socket] + client_sockets, client_sockets, [])
#     for current_socket in rlist:
#         if current_socket is server_socket:
#             connection, client_address = current_socket.accept()
#             print("New client joined!", client_address)
#             client_sockets.append(connection)
#             print_client_sockets(client_sockets)
#         else:
#             data = current_socket.recv(MAX_MSG_LENGTH).decode()
#             if data == "":
#                 print("Connection closed", )
#                 client_sockets.remove(current_socket)
#                 current_socket.close()
#                 print_client_sockets(client_sockets)
#             else:
#                 messages_to_send.append((current_socket, data))

#     for message in messages_to_send:
#         current_socket, data = message
#         if current_socket in wlist:
#             current_socket.send(data.encode())
#             messages_to_send.remove(message)
            
            

    
