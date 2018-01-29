import socket
from objects import *
import pickle
from common import *
from interface import Interface, Personnage
import pygame
from pygame.locals import *
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024



class Client:
    def __init__(self):
        self.sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dimensions = None
        self.etat = Etat.Initialisation
        self.position_start = None
        self.interface = Interface()

    def connect(self):
        self.sock.connect((TCP_IP, TCP_PORT))
        # self.sock.setblocking(0)
        self.sock.settimeout(SOCK_TIMEOUT)
    def send(self, data):
        # self.sock.send(data.encode())
        send_command(self.sock, data)

    def recv(self):
        return recv_command(self.sock)

    def close(self):
        self.sock.close()

    def tir(self,x ,y):
        vect_x = x - self.interface.perso.position.x
        vect_y = y - self.interface.perso.position.y
        self.send(Tir(Position(vect_x,vect_y)))



client = Client()
client.connect()

quit=False

while not quit:
    command = client.recv()
    if command != None:
        if client.etat == Etat.Initialisation:
            if isinstance(command, Dimensions):
                client.dimensions = command
                client.interface.update_dimensions(command)
            elif isinstance(command, Position):
                client.position_start = command
                client.interface.update_position(command)
            elif isinstance(command, Enemi):
                # client.perso.set_position(command)
                # client.interface.update_position(command)
                print("Enemi position : {} , {}".format(command.position.x, command.position.y))
                client.interface.add_enemi(command)

            elif isinstance(command, Start):
                client.etat = Etat.Pret
            else:
                print("Unknown command in state init")
        elif client.etat == Etat.Pret:
            if isinstance(command, Position):
                # client.perso.set_position(command)
                client.interface.update_position(command)
            elif isinstance(command, Enemi):
                # client.perso.set_position(command)
                # client.interface.update_position(command)
                # print("Enemi position : {} , {}".format(command.position.x, command.position.y))
                client.interface.update_enemi(command)

            else:
                print("Unknown command in state pret")

    if client.etat != Etat.Initialisation:
        move_down = False
        move_up = False
        move_right = False
        move_left = False
        for event in pygame.event.get():  # Attente des événements
            if event.type == QUIT:
                quit = True
            if event.type == MOUSEMOTION:  # Si mouvement de souris
                x = event.pos[0]
                y = event.pos[1]
                client.interface.update_position_souris(Position(x, y))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Si clic gauche
                    x = event.pos[0]
                    y = event.pos[1]
                    client.tir(x,y)
                    print("booum !")

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                client.send(Move(DOWN_RIGHT))
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                client.send(Move(DOWN_LEFT))
            else:
                client.send(Move(DOWN))
        elif pygame.key.get_pressed()[pygame.K_UP]:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                client.send(Move(UP_RIGHT))
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                client.send(Move(UP_LEFT))
            else:
                client.send(Move(UP))
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                client.send(Move(RIGHT))
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            client.send(Move(LEFT))





client.close()
