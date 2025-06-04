import threading

FORMAT = "utf-8"

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
                    conn.send(f"[GLOABAL from {msg[1]}] {msg[0]}".encode(FORMAT))
            else:
                break
                   