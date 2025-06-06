import socket
import threading
import queue
import global_handler as gh
import random

HOST = "127.0.0.1"
PORT = 65460
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ECHO_FLAG = "!ECHO"
PRIVATE_MESSAGE_FLAG = "!PM"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr, queue, conn_dict, username):
    print(f"[NEW CONNECTION] {addr}||{username} connected")
    queue.put((f"{username} Connected!", "SERVER"))
    connected = True
    while connected:
        msg = recv_msg(conn)
        print(f"[{username}] {msg}")
        
        if (msg == DISCONNECT_MESSAGE):
            connected = False
            print(f"[DISCONNECT] {addr}||{username} disconnected")
            gh.send_msg(DISCONNECT_MESSAGE, conn)
            queue.put((f"{username} Disconnected", "SERVER"))
        elif(msg == ECHO_FLAG):
            gh.send_msg("Message:", conn)
            msg = recv_msg(conn)
            gh.send_msg(f"[SERVER] you Said: {msg}\n", conn)
        elif(msg == PRIVATE_MESSAGE_FLAG):
            gh.send_msg("to whom?", conn)
            name = recv_msg(conn).strip()
            if name in conn_dict.keys():
                msg = recv_msg(conn)
                queue.put((msg, username, name))
            else:
                gh.send_msg("Not A Valid Username!", conn)

        else:
            queue.put((msg, username))

    conn_dict.pop(username)
    conn.close()


def start():
    server.listen()
    print(f"[SERVER] server is listening on {HOST}")

    active_conn_dict = {}
    global_queue = queue.Queue()

    global_hand = gh.global_handler(global_queue, active_conn_dict)

    global_hand.start()

    names = get_usernames()

    while True:
        conn, addr = server.accept()
        username = get_rand_name(names)
        while username in active_conn_dict.keys():
            username = get_rand_name(names)
        active_conn_dict[username] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr, global_queue, active_conn_dict, username))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
    
def recv_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg

def get_usernames():
    names = []
    with open("usernames.txt") as u:
        for name in u:
            names.append(name.strip())
    return names

def get_rand_name(names):
    randI = random.randint(0, len(names) - 1)
    return names[randI]

print("[START] Server is Starting...")
start()