import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"  # Local Host server 127.0.0.1 localhost

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


""" Here is the explanation for the code above:
1. The open_client_sockets list holds all the sockets that are connected to the server.
2. The select module holds the select method, which allows us to know which sockets are ready for reading.
3. The select method receives three lists of sockets: the first is the list of sockets that are waiting to be
read, the second is the list of sockets that are waiting to be written to, and the third is the list of sockets
that are in error.
4. The select method also receives a timeout argument, which is the number of seconds it will wait until
raising a TimeoutError exception if no sockets are ready. If the timeout argument is omitted, the select
method will wait until at least one socket is ready.
5. The select method returns three lists of sockets: the first is the list of sockets that are ready for reading,
the second is the list of sockets that are ready for writing, and the third is the list of sockets that are in
error.
6. The select method can be used to wait for reading and writing separately, but in our case we want to
wait for both reading and writing so we pass the list of open sockets to both the first and second
arguments.
7. The select method returns the lists of sockets that are ready for reading and writing, so we assign them
to the rlist and wlist variables, respectively.
8. We iterate over the rlist list and read data from each socket using the recv method.
9. The recv method returns an empty string if the socket was closed by the client, so we remove that
socket from the open_client_sockets list.
10. If the recv method returns a non-empty string, we assume the client is still connected and we append
the data we read to the data_to_send list.
11. """
