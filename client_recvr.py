import threading

FORMAT = "utf-8"
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"

class client_recvr(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        connected = True
        while connected:
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print("Good Bye!")
                else:
                    print(f"\n{msg}")