# Exercice - 12.2, 12.4

import socket
import select
import msvcrt

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()  # Similar to "0.0.0.0 - localhost"

# set port number
port = 5555

# connect to the server
client_socket.connect((host, port))
print("Connected to server")

while True:
    if msvcrt.kbhit():
        input = msvcrt.getch().decode()
        print(input)
        
        if not input:
            # send termination message to the server
            client_socket.send(b"terminate")
            # close the socket connection
            client_socket.close()
            break
            
        client_socket.send(input.encode())
        
    # Check if there is a message from the server
    rlist, wlist, xlist = select.select([client_socket], [], [])
    for current_socket in rlist:
        data = current_socket.recv(1024).decode()
        if data == "":
            print("Connection closed", )
            # client_sockets.remove(current_socket)
            current_socket.close()
        else:
            print(data)
    
    # if msvcrt.kbhit():
    #     input = msvcrt.getch().decode()
    #     print(input)
    #     client_socket.send(input.encode())
    #     if not input:
    #         # send termination message to the server
    #         client_socket.send(b"terminate")
    #         # close the socket connection
    #         client_socket.close()
    #         break
    # else:
    #     print("No input")
    
    #
            
        
    # get input from user
    # input_name = input("Enter text: ")
    

    # check if input is empty
    # if not input_name:
    #     # send termination message to the server
    #     client_socket.send(b"terminate")
    #     # close the socket connection
    #     client_socket.close()
    #     break

    # send input to the server
    


    # receive response from the server
    # response = client_socket.recv(1024).decode()

    # print the response
    # print(response)
