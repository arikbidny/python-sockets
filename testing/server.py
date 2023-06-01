# importing the necessary modules.
import socket
import select

# defining the header length.
HEADER_LENGTH = 10

# defining the IP address and Port Number.
IP = "127.0.0.1"
PORT = 5555

"""
Creating a server socket and providing the address family (socket.AF_INET) and type of connection (socket.SOCK_STREAM), i.e. using TCP connection.
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Modifying the socket to allow us to reuse the address. We have to provide the socket option level and set the REUSEADDR (as a socket option) to 1 so that address is reused.
"""
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binding the socket with the IP address and Port Number.
server_socket.bind((IP, PORT))

# Making the server listen to new connections.
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# A set to contain the connected clients.
clients = {}

admins = ["admin1", "admin2"]

print(f'Listening for connections on IP = {IP} at PORT = {PORT}')


def get_all_admins():
    return ", ".join(admins)


# A function for handling the received message.
def receive_message(client_socket):
    try:
        """
        The received message header contains the message length, its size is defined, and the constant.
        """
        message_header = client_socket.recv(HEADER_LENGTH)

        print(message_header.decode("utf-8"))

        """
        If the received data has no length then it means that the client has closed the connection. Hence, we will return False as no message was received.
        """
        if not len(message_header):
            return False

        # print(message_header)

        # Convert header to an int value
        message_length = int(message_header.decode('utf-8').strip())

        # Returning an object of the message header and the data of the message data.
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


# running an infinite loop to accept continuous client requests.
while True:
    # Read the data using a select module from the socketLists.
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # Iterating over the notified sockets.
    for notified_socket in read_sockets:
        """
        If the notified socket is a server socket then we have a new connection, so add it using the accept() method.
        """
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            # Else the client has disconnected before sending his/her name.
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # checkAdminUser = user['data'].decode("utf-8")

            # # check if the user is admin
            # if checkAdminUser in admins:
            #     print("is admin")
            #     print(
            #         f'Accepted new connection from {client_address[0]}:{client_address[1]} username: {user["data"].decode("utf-8")} as admin')
            # else:
            #     print("not admin")
            #     print(
            #         f'Accepted new connection from {client_address[0]}:{client_address[1]} username: {user["data"].decode("utf-8")}')

            # Adding the accepted socket to select.select() list.
            sockets_list.append(client_socket)

            # Also adding the username and username header.
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(
                *client_address, user['data'].decode('utf-8')))

        # Else the existing socket is sending a message so handling the time client.
        else:
            userName = user['data'].decode("utf-8")

            # Receiving the message.
            message = receive_message(notified_socket)

            # If no message is accepted then finish the connection.
            if message is False:
                print('Closed connection from: {}'.format(
                    clients[notified_socket]['data'].decode('utf-8')))

                # Removing the socket from the list of the socket.socket()
                sockets_list.remove(notified_socket)

                # Removing the user from the list of users.
                del clients[notified_socket]

                continue

            # Getting the user by using the notified socket, so that the user can be identified.
            user = clients[notified_socket]

            new_message = message["data"].decode("utf-8")

            if (new_message == "quit"):
                print(f'Client {user["data"].decode("utf-8")} disconnected')
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()
                # send message to all users that the user has disconnected
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(
                            user['header'] + user['data'] + message['header'] + message['data'])

                continue

            print(
                f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterating over the connected clients and broadcasting the message.
            for client_socket in clients:
                # Sending to all except the sender.

                if client_socket != notified_socket:
                    """
                    Reusing the message header sent by the sender, and saving the username header sent by the user when he/she connected.
                    """
                    # check if the user is admin
                    checkAdminUser = user['data'].decode("utf-8")
                    if checkAdminUser in admins:
                        print("is admin")
                        # send message with user name looks like 14:40 @admin1 : "message"
                        client_socket.send(
                            user['header'] + user['data'] + message['header'] + message['data'])

                    else:
                        print("not admin")
                        # print(get_all_admins())
                        client_socket.send(
                            user['header'] + user['data'] + message['header'] + message['data'])


## TODO ##
# 1. TO check if the user is admin or not and then send the message accordingly. - 14:40 @admin1 : "message"
# 2. To Create private chat between two users.
# 3. if the client sends a message: view-managers then the server should send a message to the client with the list of all the managers.
