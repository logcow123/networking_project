import threading

FORMAT = "utf-8"
HEADER = 64

class client_recvr(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(FORMAT)
                print(f"\n{msg}")