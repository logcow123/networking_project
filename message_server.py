import socket
import threading
import queue
import global_handler as gh

HOST = "127.0.0.1"
PORT = 65462
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
GLOBAL_FLAG = "!GLOBAL"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr, queue, conn_set):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg = recv_msg(conn)
        print(f"[{addr}] {msg}")
        
        if (msg == DISCONNECT_MESSAGE):
            connected = False
        elif(msg == GLOBAL_FLAG):
            gh.send_msg("Enter Your Global Message:\n", conn)
            msg = recv_msg(conn)
            queue.put((msg, addr))
        else:
            gh.send_msg(f"[SERVER] you Said: {msg}\n", conn)
    conn_set.remove(conn)
    conn.close()


def start():
    server.listen()
    print(f"[SERVER] server is listening on {HOST}")

    active_conn_set = []
    global_queue = queue.Queue()

    global_hand = gh.global_handler(global_queue, active_conn_set)

    global_hand.start()

    while True:
        conn, addr = server.accept()
        active_conn_set.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, global_queue, active_conn_set))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
    
def recv_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg



print("[START] Server is Starting...")
start()