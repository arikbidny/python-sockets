import socket
import select


class Server:
    def __init__(self, ip="0.0.0.0", port=5050):
        '''Server Constructor. If __init__ return None, then you can use
           self.error to print the specified error message.'''

        # Error message.
        self.error = ""

        # Creating a socket object.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Trying to bind it.
        try:
            self.server.bind((ip, port))
            pass

        # Failed, because socket has been shuted down.
        except OSError:
            self.error = "The server socket has been shuted down."

        # Failed, because socket has been forcibly reseted.
        except ConnectionResetError:
            self.error = "The server socket has been forcibly reseted."

        # Start Listening.
        self.server.listen()

        # _____Other Variables_____#

        # A flag to know when to shut down thread loops.
        self.running = True

        # Store clients here.
        self.sockets = [self.server]

        # _____Other Variables_____#

        # Start Handling the sockets.
        self.handleSockets()


# Handle Sockets.
def handleSockets(self):

    while True:
        r, w, x = select.select(self.sockets, [], self.sockets)

        # If server is ready to accept.
        if self.server in r:

            client, address = self.server.accept()
            self.sockets.append(client)

        # Elif a client send data.
        elif len(r) > 0:

            # Receive data.
            try:
                data = r[0].recv(1024)

            # If the client disconnects suddenly.
            except ConnectionResetError:
                r[0].close()
                self.sockets.remove(r[0])
                print("A user has been disconnected forcible.")
                continue

            # Connection has been closed or lost.
            if len(data) == 0:

                r[0].close()
                self.sockets.remove(r[0])
                print("A user has been disconnected.")

            # Else send the data to all users.
            else:

                # For all sockets except server.
                for client in self.sockets[1:]:

                    # Do not send to yourself.
                    if client != r[0]:
                        client.send(data)


server = Server()
print("Errors:", server.error)
