# Exercice - 12.2, 12.4

import socket
import select

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()  # Similar to "0.0.0.0 - localhost"

# set port number
port = 5555

# connect to the server
client_socket.connect((host, port))


def send_message():
    while True:
        try:
            # Use select to monitor stdin for input events
            _, write_sockets, _ = select.select([], [client_socket], [])

            for sock in write_sockets:
                message = input()
                client_socket.send(message.encode())
        except:
            # If there is an error sending the message, assume the server is disconnected
            client_socket.close()
            break


def read_message():
    while True:
        try:
            # Use select to monitor socket for read events
            read_sockets, _, _ = select.select([client_socket], [], [])

            for sock in read_sockets:
                message = sock.recv(4096).decode()
                print(message)
        except:
            # If there is an error receiving the message, assume the server is disconnected
            client_socket.close()
            break


read_message()
send_message()

# while True:
#     # get input from user
#     input_name = input("Enter message: ")

#     # check if input is empty
#     if not input_name:
#         # send termination message to the server
#         client_socket.send(b"terminate")
#         # close the socket connection
#         client_socket.close()
#         break

#     # send input to the server
#     client_socket.send(input_name.encode())

#     # receive response from the server
#     response = client_socket.recv(1024).decode()

#     # print the response
#     print(response)
