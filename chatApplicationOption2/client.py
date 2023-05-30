import socket
import select
import sys
import time
import msvcrt

# Function to display prompt and receive user input
def prompt():
    sys.stdout.write('You: ')
    sys.stdout.flush()

# Main function to handle client connections
def main():
    # if len(sys.argv) < 3:
    #     print('Usage: python client.py hostname port')
    #     sys.exit()

    host = "127.0.0.1"
    port = 1234

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect to the server
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. Start sending messages.')
    prompt()

    while True:
        socket_list = [s]

        # Get the list of sockets ready for reading
        _, write_sockets, _ = select.select([], socket_list, [])

        if msvcrt.kbhit():
            # User entered a message
            msg = sys.stdin.readline().strip()
            s.sendall(msg.encode())

            if msg == 'quit':
                break

        if s in write_sockets:
            try:
                data = s.recv(4096).decode()
                if not data:
                    print('\nDisconnected from chat server')
                    break
                else:
                    sys.stdout.write(data + '\n')
                    prompt()
            except socket.error:
                print('\nDisconnected from chat server')
                break

if __name__ == "__main__":
    main()
