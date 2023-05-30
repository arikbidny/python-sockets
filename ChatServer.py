import select
import socket

HOST = '0.0.0.0'
PORT = 5555

# Create a socket object and bind it to a specific address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Listening for clients...")

# Create a list to keep track of connected clients
clients = [server_socket]

# Create a dictionary to keep track of messages sent to each client
sent_messages = {}

while True:
    # Use the select library to wait for input from the sockets in the clients list
    read_sockets, _, _ = select.select(clients, [], [])

    for client_socket in read_sockets:
        # If the client_socket is the server_socket, a new client is connecting
        if client_socket == server_socket:
            # Accept the new connection and add the client to the clients list
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            sent_messages[client_socket] = []

            print(f'New client connected: {client_address}')

        # Otherwise, a message is being received from an existing client
        else:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(
                        f'Received message from {client_socket.getpeername()}: {message}')

                    # Send the message to all clients except the sender
                    for client in clients:
                        if client != server_socket and client != client_socket:
                            if client_socket not in sent_messages[client]:
                                client.sendall(message.encode())
                                sent_messages[client].append(client_socket)

            except:
                # If an error occurs, the client is disconnected
                print(f'Client {client_socket.getpeername()} disconnected')
                clients.remove(client_socket)
                del sent_messages[client_socket]
                client_socket.close()
