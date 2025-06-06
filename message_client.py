import socket
import client_recvr as cr

HOST = "127.0.0.1"
PORT = 65462
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
GLOBAL_FLAG = "!GLOBAL"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    pass
    client.connect((HOST, PORT))
    recvr = cr.client_recvr(client)
    recvr.start()

    connected = True
    while connected:
        msg = input("")
        send_msg(msg)
        if msg == DISCONNECT_MESSAGE:
            connected = False
    recvr.join()



def send_msg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

if __name__ == "__main__":
    main()