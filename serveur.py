import numpy as np
import socket
from objects import *
import time
from common import *
from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20
HEIGHT = 480
WIDTH = 640



# class Command:
#     def __init__(self, player, cmd):
#         self.player = player
#         self.cmd = cmd
#
#     def process(self):
#         self.player.send_command(self.cmd)

class CmdMove(Thread):
    def __init__(self, player, dir):
        Thread.__init__(self)
        self.player = player
        self.dir = dir

    def run(self):
        self.player.move(self.dir)
        enemi = self.player
        for p in serv.players:
            if p.addr != enemi.addr:
                p.send_enemi_position(enemi)

class CmdTir(Thread):
    def __init__(self, player, vect_dir):
        Thread.__init__(self)
        self.player = player
        self.vect_dir = vect_dir

    def run(self):
        print("send in dir {},{}".format(self.vect_dir.x, self.vect_dir.y))
        # self.player.move(self.dir)
        # enemi = self.player
        # for p in serv.players:
        #     if p.addr != enemi.addr:
        #         p.send_enemi_position(enemi)


class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.score = 0

        self.set_dimension()

    def send_command(self, command):
        send_command(self.conn, command)

    def send_enemi_position(self, p):
        self.send_command(Enemi(p.addr, Position(p.x, p.y)))

    def move(self, dir):
        print("dir = {}".format(dir))
        print("x = {} y = {}".format(self.x, self.y))
        if (dir == UP or dir == UP_LEFT or dir == UP_RIGHT) and self.y >0:
            self.y -=1
        if (dir == DOWN or dir == DOWN_RIGHT or dir == DOWN_LEFT) and self.y<HEIGHT-1:
            self.y +=1
        if (dir == LEFT or dir == UP_LEFT or dir == DOWN_LEFT) and self.x >0:
            self.x -=1
        if (dir == RIGHT or dir == UP_RIGHT or dir == DOWN_RIGHT) and self.x<WIDTH-1:
            self.x +=1
        print("new x = {} y = {}".format(self.x, self.y))
        self.send_command(Position(self.x, self.y))



    def recv(self):
        return self.conn.recv(BUFFER_SIZE)

    def set_dimension(self):
        self.send_command(Dimensions(WIDTH, HEIGHT))

    def position_set(self, x, y):
        self.x, self.y = x,y
        self.send_command(Position(x, y))

    def position_get(self):
        return self.x, self.y

    def close(self):
        self.send_command(Quit())
        self.conn.close()


class Server:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((TCP_IP, TCP_PORT))
        self.players = list()

    def add_player(self):
        self._sock.listen(1)
        conn, addr = self._sock.accept()
        # conn.setblocking(0)
        conn.settimeout(SOCK_TIMEOUT)
        self.players.append(Player(conn,addr))

    def close(self):
        for p in self.players:
            p.close()
        self._sock.close()

# command_pile = []
#
# class CommandProcessing(Thread):
#     def __init__(self, command_pile):
#         Thread.__init__(self)
#         self.pile = command_pile
#
#     def run(self):
#         while 1:
#             if len(self.pile):
#                 cmd = self.pile.pop()
#                 cmd.process()
#
# cmd_process = CommandProcessing(command_pile)
# cmd_process.start()

serv = Server()
# Les joueurs se connectent
serv.add_player()
serv.add_player()

serv.players[0].position_set(5, HEIGHT/2)
serv.players[1].position_set(WIDTH-150, HEIGHT/2)

serv.players[0].send_enemi_position(serv.players[1])
serv.players[1].send_enemi_position(serv.players[0])



for p in serv.players:
    p.send_command(Start())


while 1:
    for p in serv.players:
        command = recv_command(p.conn)
        if command != None:
            if isinstance(command, Move):
                # p.move(command.dir)
                # # on previent les autres joueurs que ce mec a bougé
                # enemi = p
                # for p in serv.players:
                #     if p.addr != enemi.addr:
                #         p.send_enemi_position(enemi)
                # command_pile.append(CmdMove(p, command.dir))
                cmd_move = CmdMove(p, command.dir)
                cmd_move.start()
            elif isinstance(command, Tir):
                cmd_tir = CmdTir(p, command.vect_direction)
                cmd_tir.start()


serv.close()



