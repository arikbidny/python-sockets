import select
import socket
import datetime


class ChatServer:
    def __init__(self):
        self.users = {}  # משתמשים רשומים: {socket: username}
        self.admins = ['admin1', 'admin2', 'admin3']  # רשימת המנהלים
        self.messages = []  # רשימת הודעות

    def process_message(self, sender):
        message = sender.recv(1024).decode().strip()
        if message == "quit":
            self.disconnect_user(sender)
        elif message == "view-managers":
            self.send_private_message(
                "Managers: " + ', '.join(self.admins), sender)
        elif message.startswith('!'):  # הודעה פרטית
            recipient, msg = self.extract_private_message(message)
            self.send_private_message(msg, recipient)
        elif sender in self.admins and message.startswith('@'):  # הודעת מנהל
            self.send_message(message)
        else:  # הודעה רגילה
            self.send_message(message, sender)

    def send_message(self, message, sender=None):
        now = datetime.datetime.now().strftime("%H:%M")
        formatted_message = now + ' ' + self.users[sender] + ': ' + message
        self.messages.append(formatted_message)
        for user_socket in self.users.keys():
            if user_socket != sender:
                user_socket.send(formatted_message.encode())

    def send_private_message(self, message, recipient):
        now = datetime.datetime.now().strftime("%H:%M")
        formatted_message = now + ' ' + self.users[recipient] + ': ' + message
        recipient.send(formatted_message.encode())

    def extract_private_message(self, message):
        parts = message.split(' ', 1)
        recipient = parts[0][1:]
        msg = parts[1]
        return recipient, msg

    def disconnect_user(self, socket):
        username = self.users[socket]
        del self.users[socket]
        socket.close()
        self.send_message(username + ' has left the chat!')

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 1234))
        server_socket.listen(5)
        inputs = [server_socket]

        while True:
            readable, _, _ = select.select(inputs, [], [])
            for sock in readable:
                if sock is server_socket:
                    client_socket, address = server_socket.accept()
                    inputs.append(client_socket)
                    client_socket.send("Enter your username: ".encode())
                else:
                    try:
                        self.process_message(sock)
                    except ConnectionResetError:
                        self.disconnect_user(sock)
                        inputs.remove(sock)


# run the server
server = ChatServer()
server.run()
