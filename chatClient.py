import socket
import select
import msvcrt

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set port number
port = 5555

# connect to the server
client_socket.connect((host, port))

# set the socket to non-blocking mode
client_socket.setblocking(False)

# set the username for the client
username = input("Enter your username: ")
client_socket.send(username.encode())

# define a function for sending messages


def send_message():
    message = input("Enter message: ")
    if message:
        client_socket.send(message.encode())


while True:
    # use msvcrt module to check if a key has been pressed
    if msvcrt.kbhit():
        # if a key has been pressed, read the key and send the message
        msvcrt.getch()
        send_message()

    # select the sockets that are ready to be read
    read_sockets, _, exception_sockets = select.select(
        [client_socket], [], [client_socket])

    # iterate over the sockets that are ready to be read
    for socket in read_sockets:
        # receive message from server and print it
        message = socket.recv(1024).decode()
        print(message)

    # handle exceptions
    for socket in exception_sockets:
        print("Error: Failed to receive data from server.")
        client_socket.close()
        exit()
