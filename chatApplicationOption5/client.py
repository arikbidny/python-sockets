import select
import socket
import msvcrt


class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 1234))

    def run(self):
        while True:
            readable, _, _ = select.select([self.client_socket], [], [], 0)

            if self.client_socket in readable:
                message = self.client_socket.recv(1024).decode()
                print(message)

            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode()
                if user_input == 'q':
                    break
                self.client_socket.send(user_input.encode())

        self.client_socket.close()


client = ChatClient()
client.run()
