import socket
import select
import tkinter as tk
from tkinter import messagebox

# Create a Tkinter application window
window = tk.Tk()
window.title("Chat Client Advanced Ui by Yuval")
window.geometry("800x600")

# Create a text area for displaying messages
message_text = tk.Text(window)
message_text.pack(fill=tk.BOTH, expand=True)
message_text.configure(state="disabled")

# Global variable to store the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))


# Get the username from the user
def get_username():
    # global client_socket

    username = username_entry.get()
    print("username: ", username)
    if username:
       client_socket.send(username.encode())
       start_client(client_socket)
    else:
        messagebox.showerror("Error", "Please enter a username.")


# Connect to the server
def connect_to_server(username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    # Receive username input from the user
    client_socket.send(username.encode())

    # Start the client loop
    start_client(client_socket)
    return client_socket


# Send chat message to the server
def send_chat_message():
    # global client_socket
    message = message_entry.get()
    print("message: ", message)
    username = username_entry.get()
    print(client_socket)
    
    if message:
        # client_socket = connect_to_server(username)
        send_chat_message_to_server(client_socket, message)
    else:
        messagebox.showerror("Error", "Please enter a message.")


def send_chat_message_to_server(client_socket, message):
    client_socket.send(message.encode())


def start_client(client_socket):
    while True:
        # Check if there is incoming data from the server
        if client_socket in select.select([client_socket], [], [], 0)[0]:
            data = client_socket.recv(1024).decode()
            message_text.configure(state="normal")
            message_text.insert(tk.END, data + "\n")
            message_text.configure(state="disabled")
            message_text.see(tk.END)

        window.update_idletasks()
        window.update()


# Create and pack the username label and entry
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

# Create and pack the connect button
connect_button = tk.Button(window, text="Connect", command=get_username)
connect_button.pack()

# Create and pack the message entry and send button
message_label = tk.Label(window, text="Message:")
message_label.pack()
message_entry = tk.Entry(window)
message_entry.pack()

send_button = tk.Button(window, text="Send", command=send_chat_message)
send_button.pack()

# Start the Tkinter event loop
window.mainloop()
