import socket
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Connected to server. Type 'q' to quit.")

while True:
    # Check if there is any keyboard input
    if select.select([client_socket], [], [], 0.1)[0]:
        try:
            # Read user input
            user_input = input()

            # If 'q' is entered, break the loop and quit
            if user_input == 'q':
                break

            # Send the user input as a request to the server
            client_socket.send(user_input.encode())

        except KeyboardInterrupt:
            break

    # Check if there is any incoming data from the server
    if select.select([client_socket], [], [], 0.1)[0]:
        data = client_socket.recv(1024).decode()
        print("Response from server:", data)

client_socket.close()
