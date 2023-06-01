import socket
import threading

from tkinter import *


class Client:
    # Send the message.
    def sendMSG(self):
        self.server.send(str.encode(self.msg.get()))

    # Receive message.

    def recvMSG(self):

        while self.running:

            data = self.server.recv(1024)

            print(bytes.decode(data))


# New client.
main = Client()
print("Errors:", main.error)


# Start a thread with the recvMSG method.
thread = threading.Thread(target=main.recvMSG)
thread.start()

# Start the gui.
main.startGUI()

# Close the connection when the program terminates and stop threads.
main.running = False
main.server.close()
