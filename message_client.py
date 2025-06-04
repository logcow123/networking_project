import socket

HOST = "127.0.0.1"
PORT = 65462
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
GLOBAL_FLAG = "!GLOBAL"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_msg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

input("Wait for GLobal SEND")
send_msg(GLOBAL_FLAG)
print(client.recv(1024).decode(FORMAT))
print(client.recv(1024).decode(FORMAT))