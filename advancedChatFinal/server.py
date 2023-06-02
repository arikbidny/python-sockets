import socket
import select
import datetime
import re


MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"  # Local Host server

print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print("Listening for clients...")
client_sockets = []
# open_client_sockets = []
# messages_to_send = []

clients = {}

# List of admins
admins = ['admin1', 'admin2']

# Dictionary to store muted users
muted_users = {}

# List to store private chats
private_chats = []


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print(c.getpeername())
        
def send_message(client, message):
    client.send(message.encode())
        
        
def broadcast_global_message(message):
    for client in clients.values():
        client.send(message.encode())
        
# Broadcast message to all connected clients
def broadcast(message, username):
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    if (username in admins):
        for client in clients.values():
          print(client)
          message = f"{time_str} @{username}: {message}"
          client.send(message.encode())
    else:
        for client in clients.values():
            print(client)
            # send message with username and message hour and minutes HH:mm
            message = f"{time_str} {username}: {message}"
            client.send(message.encode())

# get all admins 
def get_admins():
    admins_str = "Admins: "
    for admin in admins:
        admins_str += f"{admin} "
    return admins_str 

# give admin permissions to client
def give_admin_permissions(admin, user):
    if admin in admins:
        admins.append(user)
        broadcast_global_message(f"{user} has been granted admin permissions!")
    else:
        current_socket.send("You don't have admin permissions!".encode())
        
# Process kick user command
def process_kick_user(admin, user):
    if admin in admins:
        client_sockets.remove(current_socket)
        clients.pop(username)
        broadcast_global_message(f"{user} has been kicked from the chat!")
        
def process_mute_user(admin, user):
    if admin in admins:
        muted_users[user] = True
        send_message(clients[user], "You cannot speak here")
        
def process_private_message(sender, recipient, message):
    if sender in clients and recipient in clients:
        private_message = f"Private message from {sender}: {message}"
        send_message(clients[recipient], private_message)

# New Client -> Open a new socket connection
# Existing Client -> Read the name and print to the command line


while True:
    rlist, wlist, xlist = select.select(
        [server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            print("New connection")
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            
            username = connection.recv(1024).decode().strip()

            print(f"Username in first connection: {username}")

            clients[username] = connection;
            
            print(f"New client connected: {username}")
            
            # Broadcast user join message
            broadcast_global_message(f"{username} has joined the chat!")      
            
            
            # print_client_sockets(client_sockets)
        else:
            print("Incoming message from a client")
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M")
            # Check if the user disconnected from the server
            if not data:
                print("Connection closed", )
                client_sockets.remove(current_socket)
                clients.pop(username)
                broadcast_global_message(f"{time_str} {username} has left the chat!") 
                # current_socket.close()
                # print_client_sockets(client_sockets)
                continue
            if data == "" or data == "quit":
                print(f"Connection closed for {username}", )
                client_sockets.remove(current_socket)
                clients.pop(username)
                # current_socket.close()
                broadcast_global_message(f"{time_str} {username} has left the chat!") 
                # print_client_sockets(client_sockets)
            if data == "view-managers":
                print("View managers")
                current_socket.send(get_admins().encode())
            else:       
                username_length = int(data[0])
                
                username_send =  ''.join(data[1 : username_length + 1])

                command = int(data[username_length + 1])
                
                # message_length = int(data[username_length + 2 : username_length + 2 + command])

                # message = data[username_length + 2 + command :]
                # get the message from the data
                match = re.match(r"\d+[A-Za-z]+\d+(.*)", data)
                
                if match:
                    message = match.group(1)
                    print(f"Command: {command}")
                    # print(f"CommandTest: {commandTest}")
                    print(f"Message: {message}")
                    # regular chat message
                    if command == 1:
                        print("Regular message")
                        print(username_send)
                        broadcast(message, username_send)  
                        # continue  
                    # give admin permission 
                    if command == 2:
                        print("give admin access")
                        give_admin_permissions(username_send, message)
                        # continue
                    # kick a user by admin
                    elif command == 3:
                        print("kick user from the chat")
                        process_kick_user(username_send, message)
                        # continue
                    # Mute a user
                    elif command == 4:
                        print("mute user from the chat")
                        process_mute_user(username_send, message)
                    # Private chat
                    elif command == 5:
                        print("private chat")
                        message_length = int(data[username_length+2:username_length+2+command])
                        recipient_length = int(data[4+username_length+message_length])
                        recipient = data[5+username_length+message_length:5+username_length+message_length+recipient_length]
                        private_message = data[5+username_length+message_length+recipient_length:]
                        process_private_message(username, recipient, private_message)                        
                else:
                    print("Invalid input format")
                        
                    
                
                # messages_to_send.append((current_socket, data))
                # print(data)

    # for message in messages_to_send:
    #     current_socket, data = message
    #     if current_socket in wlist:
    #         current_socket.send(data.encode())
    #         messages_to_send.remove(message)