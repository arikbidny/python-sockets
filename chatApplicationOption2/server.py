import socket
import select
import sys
import time

# List of connected clients
clients = []
admins = ['admin1', 'admin2']  # Hardcoded list of admin usernames
muted_users = set()  # Set to store muted users
user_map = {}  # Dictionary to store usernames and corresponding sockets


# Function to broadcast chat messages to all connected clients
def broadcast_message(sender, message):
    current_time = time.strftime('%H:%M', time.localtime())

    # Add timestamp and username to the message
    message = f'{current_time} {sender}: {message}'

    for client in clients:
        # Send the message to all clients except the sender
        if client != sender:
            client.send(message.encode())
            
            
# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client 
            message = client_socket.recv(4096).decode()
            
            if message:
                if message.startswith('@') and client_socket in user_map.values():
                    # Check if the sender is an admin
                    if user_map[client_socket] in admins:
                        # Extract the username and message content
                        parts = message.split(' ', 1)
                        if len(parts) > 1:
                            username = parts[0][1:]
                            content = parts[1]
                            if username in user_map.values():
                                # Send the message to the specified user
                                for sock, user in user_map.items():
                                    if user == username:
                                        sock.send(f'{user_map[client_socket]} (private): {content}'.encode())
                                        break
                            else:
                                client_socket.send(f'{username} is not connected.'.encode())
                        else:
                            client_socket.send('Invalid command format.'.encode())                      
                    else:
                        client_socket.send('You are not authorized to send admin messages.'.encode())
                elif message.startswith('!'):
                    # Private message
                    parts = message.split(' ', 1)
                    if len(parts) > 1:
                        recipient_username, content = parts[0][1:], parts[1]
                        recipient_socket = None

                        # Find the recipient's socket
                        for sock, user in user_map.items():
                            if user == recipient_username:
                                recipient_socket = sock
                                break
                            
                        if recipient_socket:
                            # Send the private message to the recipient
                            sender_username = user_map[client_socket]
                            recipient_socket.send(f'{sender_username} (private): {content}'.encode())
                            client_socket.send(f'To {recipient_username} (private): {content}'.encode())
                        else:
                            client_socket.send(f'{recipient_username} is not connected.'.encode())
                    else:
                        client_socket.send('Invalid command format.'.encode())
                elif message == 'quit':
                    # Disconnect the client
                    username = user_map[client_socket]
                    broadcast_message(client_socket, f'{username} has left the chat!')
                    remove_client(client_socket)
                    break
                else:
                    # Broadcast the message to all connected clients
                    sender_username = user_map[client_socket]
                    broadcast_message(client_socket, message)
            else:
                # Disconnect the client
                username = user_map[client_socket]
                broadcast_message(client_socket, f'{username} has left the chat!')
                remove_client(client_socket)
                break               
            
        
        except:
            # Disconnect the client on error
            username = user_map[client_socket]
            broadcast_message(client_socket, f'{username} has left the chat!')
            remove_client(client_socket)
            break
        
# Function to add a new client to the server
def add_client(client_socket, address):
    username = client_socket.recv(4096).decode()

    # Check if the username is already taken
    if username in user_map.values():
        client_socket.send('Username is already taken. Please choose another username.'.encode())
        client_socket.close()
        return

    # Add the client to the list of connected clients
    clients.append(client_socket)
    user_map[client_socket] = username

    # Send a welcome message to the client
    client_socket.send(f'Welcome to the chat, {username}!'.encode())

    # Notify all clients about the new user
    broadcast_message(client_socket, f'{username} has joined the chat!')

    # Send the list of admins to the client
    if username in admins:
        client_socket.send('You are an admin.'.encode())
    else:
        client_socket.send('You are a normal user.'.encode())
        
        
# Function to remove a client from the server
def remove_client(client_socket):
    if client_socket in clients:
        username = user_map[client_socket]
        clients.remove(client_socket)
        del user_map[client_socket]
        client_socket.close()

        # Remove the user from the muted users set
        muted_users.discard(username)

        # Notify all clients about the user leaving
        broadcast_message(client_socket, f'{username} has left the chat!')
     

# Main function to handle server connections
def main():
    # if len(sys.argv) < 3:
    #     print('Usage: python server.py hostname port')
    #     sys.exit()

    host = "127.0.0.1"
    port = 1234

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(10)
    
 # Add the server socket to the list of sockets to be monitored
    socket_list = [server_socket]

    print('Chat server started on {}:{}'.format(host, port))

    while True:
        # Get the list of sockets ready for reading
        read_sockets, _, _ = select.select(socket_list, [], [])

        for sock in read_sockets:
            # New client connection
            if sock == server_socket:
                client_socket, address = server_socket.accept()
                add_client(client_socket, address)
            # Incoming message from a client
            else:
                handle_client(sock)

    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()