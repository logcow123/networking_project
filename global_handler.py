import threading

FORMAT = "utf-8"
HEADER = 64

class global_handler(threading.Thread):
    def __init__(self, queue, active_conn):
        super().__init__()
        # Queue should hold Tuples of the addres of the sender and the message (msg, addr)
        self.queue = queue
        #This should be a set of active connections
        self.active_conns = active_conn

    def run(self):
        while True:
            msg = self.queue.get() 
            if msg:
                for conn in self.active_conns:
                    send_msg(f"[{msg[1]}]SAID: ,{msg[0]}\n", conn)
            else:
                break
                   
def send_msg(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)
    