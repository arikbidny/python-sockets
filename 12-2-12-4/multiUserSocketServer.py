import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"  # Local Host server

print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []


open_client_sockets = []

# New Client -> Open a new socket connection
# Existing Client -> Read the name and print to the command line
while True:
    rlist, wlist, xlist = select.select(
        [server_socket] + client_sockets, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
            else:
                print(data)
