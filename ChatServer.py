import socket
import select

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set port number
port = 5555

# bind the socket to a public host and port
server_socket.bind((host, port))

# listen for incoming connections
server_socket.listen()

# create a list of sockets for select.select()
sockets_list = [server_socket]

# create a dictionary of clients with their corresponding sockets
clients = {}

# create a dictionary of clients with their corresponding private messages
private_messages = {}

print(f"Server listening on {host}:{port}...")


def receive_message(client_socket):
    try:
        # receive message from client
        message = client_socket.recv(1024)
        if message:
            # check if message is a private message
            if message.startswith(b"@"):
                # get the recipient's name and message content
                recipient_name, message_content = message.split(b" ", 1)
                recipient_name = recipient_name[1:].decode()

                # send the message to the recipient if they exist
                if recipient_name in clients:
                    recipient_socket = clients[recipient_name]
                    recipient_socket.send(
                        f"Private message from {clients[client_socket]}: {message_content.decode()}".encode())
                    private_messages[client_socket].append(recipient_name)
                else:
                    client_socket.send(
                        f"Error: {recipient_name} is not a valid recipient.".encode())
            else:
                # send message to all clients except the sender and those who already received the message privately
                for socket in clients:
                    if socket != client_socket and socket not in private_messages[client_socket]:
                        socket.send(
                            f"{clients[client_socket]}: {message.decode()}".encode())
                private_messages[client_socket] = []
        else:
            # remove the client from the list of sockets and clients
            sockets_list.remove(client_socket)
            del clients[client_socket]
            del private_messages[client_socket]
    except:
        # remove the client from the list of sockets and clients
        sockets_list.remove(client_socket)
        del clients[client_socket]
        del private_messages[client_socket]


while True:
    # select the sockets that are ready to be read
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # iterate over the sockets that are ready to be read
    for socket in read_sockets:
        # if the socket is the server socket, accept the new connection
        if socket == server_socket:
            client_socket, client_address = server_socket.accept()

            # add the new client socket to the list of sockets and clients
            sockets_list.append(client_socket)

            client_name = client_socket.recv(1024).decode()
            clients[client_socket] = client_name
            private_messages[client_socket] = []

            print(
                f"New connection from {client_address[0]}:{client_address[1]} ({client_name})")
        else:
            # receive message from client and broadcast to all clients
            receive_message(socket)

    # handle exceptions
    for socket in exception_sockets:
        sockets_list.remove(socket)
        del clients[socket]
        del private_messages[socket]
