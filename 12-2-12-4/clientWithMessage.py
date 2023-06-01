# Exercice - 12.2, 12.4

import socket

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()  # Similar to "0.0.0.0 - localhost"

# set port number
port = 5555

# connect to the server
client_socket.connect((host, port))

while True:
    # get input from user
    input_name = input("Enter message: ")

    # check if input is empty
    if not input_name:
        # send termination message to the server
        client_socket.send(b"terminate")
        # close the socket connection
        client_socket.close()
        break

    # send input to the server
    client_socket.send(input_name.encode())

    # receive response from the server
    response = client_socket.recv(1024).decode()

    # print the response
    print(response)
