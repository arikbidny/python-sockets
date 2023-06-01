import socket
import sys
import errno
import datetime
import tkinter as tk
from tkinter import messagebox

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234


class ClientUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_text = tk.Text(self.root)
        self.chat_text.pack(fill=tk.BOTH, expand=True)

        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_text)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.connect()

    def connect(self):
        self.username = tk.simpledialog.askstring(
            "Username", "Enter your username:")
        if not self.username:
            self.root.destroy()
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((IP, PORT))
            self.client_socket.setblocking(False)
            self.send_username()
            self.root.after(100, self.receive_messages)
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error",
                                 "Unable to connect to the server.")
            self.root.destroy()

    def send_username(self):
        username = self.username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + username)

    def send_message(self, event=None):
        message = self.entry_text.get()
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + message)
        self.entry_text.set("")

    def receive_messages(self):
        try:
            while True:
                username_header = self.client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    messagebox.showinfo("Connection Closed",
                                        "Connection closed by the server.")
                    self.root.destroy()
                    return

                username_length = int(username_header.decode('utf-8').strip())
                username = self.client_socket.recv(
                    username_length).decode('utf-8')

                current_time = datetime.datetime.now().strftime('%H:%M')
                message_header = self.client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.client_socket.recv(
                    message_length).decode('utf-8')

                self.chat_text.insert(
                    tk.END, f"{current_time} {username}: {message}\n")
                self.chat_text.see(tk.END)
        except (ConnectionAbortedError, ConnectionResetError):
            messagebox.showinfo("Connection Closed",
                                "Connection closed by the server.")
            self.root.destroy()
        except OSError as e:
            if e.errno == errno.EWOULDBLOCK:
                pass
            else:
                messagebox.showerror(
                    "Error", "An error occurred while receiving messages.")
                self.root.destroy()
        finally:
            self.root.after(100, self.receive_messages)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientUI(root)
    root.mainloop()
