import socket

HOST = "127.0.0.1"
PORT = 65462

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(b"Hello World!")
    data = s.recv(1024)

print(data.decode('utf-8'))