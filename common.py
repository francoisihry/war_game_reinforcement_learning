import pickle
SIZE_LEN_OBJECT = 150
SOCK_TIMEOUT = 0.01
import socket

class Etat:
    Pret = 0
    Initialisation=2
    Victoire=3
    Defaite=4

def send_command(conn, data):
    data = pickle.dumps(data).ljust(SIZE_LEN_OBJECT, b'\0')
    # d_len = pickle.dumps(len(data))
    # conn.send(d_len)
    conn.send(data)


def recv_command(sock):
    try:
        # command_len = pickle.loads(sock.recv(SIZE_LEN_OBJECT))
        return pickle.loads(sock.recv(SIZE_LEN_OBJECT))
    except socket.timeout:
        # print(e)
        return None