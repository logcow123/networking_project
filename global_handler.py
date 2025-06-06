import threading
import hangman as hang
import queue

FORMAT = "utf-8"
HEADER = 64
HANGMAN_FLAG = "!HANG"

class global_handler(threading.Thread):
    def __init__(self, queue, active_conn):
        super().__init__()
        # Queue should hold Tuples of the addres of the sender and the message (msg, username)
        self.queue = queue
        #This should be a set of active connections
        self.active_conns = active_conn

    def run(self):
        guess_queue = queue.Queue()
        hang_lock = threading.Lock()
        while True:
            msg = self.queue.get() 
            if msg:
                if len(msg) == 3:
                    if msg[2] == HANGMAN_FLAG:
                        game = hang.hangman(msg[0], guess_queue, hang_lock, self.queue, msg[1])
                        game.start()
                    else:
                        conn = self.active_conns[msg[2]]
                        send_msg(f"[{msg[1]}->{msg[2]}] {msg[0]}", conn)
                else:
                    if len(msg[0]) == 1:
                        guess_queue.put(msg[0])
                    for conn in self.active_conns.values():
                        send_msg(f"[{msg[1]}] {msg[0]}", conn)
            
                   
def send_msg(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)
    