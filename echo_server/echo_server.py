import socket


def modifyData(data):
    my_string = data.decode('utf-8')
    my_string = f"Server Says: {my_string}"
    new_data = my_string.encode('utf-8')
    return new_data

HOST = "127.0.0.1"
PORT = 65462


# creates a socket that is in IPv4(AF_INET) and TCP(SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn as c:
        print(f"Connected by: {addr}")
        while True:
            data = c.recv(1024)
            if not data:
                break
            c.sendall(modifyData(data))

