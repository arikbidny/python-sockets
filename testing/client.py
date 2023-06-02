import sys
import socket
import select
import msvcrt


def chat_client():
    server_address = ('localhost', 5555)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    try:
        # Connect to the server
        client_socket.connect(server_address)
        print("Connected to chat server.")

        # Set up a list of input sources (stdin and the socket)
        inputs = [client_socket, sys.stdin]

        while True:
            # Use select to wait for input from any source
            read_sockets, _, _ = select.select(inputs, [], [])

            for sock in read_sockets:
                if sock == client_socket:
                    # Data received from the server
                    data = sock.recv(4096)
                    if not data:
                        print("Disconnected from chat server.")
                        client_socket.close()
                        return
                    else:
                        print(data.decode(), end="")
                else:
                    # User entered a message
                    if msvcrt.kbhit():
                        message = sys.stdin.readline()
                        client_socket.send(message.encode())

    except Exception as e:
        print("Error: {}".format(str(e)))
        client_socket.close()


if __name__ == "__main__":
    chat_client()
