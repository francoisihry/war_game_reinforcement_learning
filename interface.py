import pygame
from objects import Position, Dimensions
import math


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND=BLUE

HEIGHT_ARROW = 60
WIDTH_ARROW = 10
HEIGHT_ARROW_2 = 10
WIDTH_ARROW_2 =5


class Fleche:
    def __init__(self, interface):
        self.interface = interface
        self.x_A, self.y_A = 0,0
        self.x_B, self.y_B = 0,0
        self.x_C, self.y_C = 0,0
        self.x_D, self.y_D = 0,0
        self.x_E, self.y_E = 0,0
        self.x_F, self.y_F = 0,0
        self.x_G, self.y_G = 0,0

    def _rotation(self, angle, centre, point):
        # on translate a l'origine:
        x = point.x - centre.x
        y = point.y - centre.y
        # on rotationne:
        y_new = y*math.cos(angle)-x*math.sin(angle)
        x_new = y*math.sin(angle)+x*math.cos(angle)
        # on retranslate
        x_new += centre.x+self.interface.perso.img.get_width()/2
        y_new += centre.y+self.interface.perso.img.get_height()/2

        return x_new,y_new

    def update(self):
        x = self.interface.perso.position.x
        y = self.interface.perso.position.y
        O = y - self.interface.position_souris.y
        A = self.interface.position_souris.x - x
        H = math.sqrt(O * O + A * A)
        angle = math.acos(A / H)
        if O < 0:  angle = -angle
        # self._draw(BACKGROUND)
        # print("A = {}  O = {}  H = {}  --> Angle = {}".format(A, O, H, angle))
        self.x_A, self.y_A = self._rotation(angle, Position(x, y), Position(x, y - WIDTH_ARROW / 2))
        self.x_B, self.y_B = self._rotation(angle, Position(x, y), Position(x, y + WIDTH_ARROW / 2))
        self.x_C, self.y_C = self._rotation(angle, Position(x, y), Position(x + HEIGHT_ARROW, y - WIDTH_ARROW / 2))
        self.x_D, self.y_D = self._rotation(angle, Position(x, y), Position(x + HEIGHT_ARROW, y + WIDTH_ARROW / 2))
        self.x_E, self.y_E = self._rotation(angle, Position(x, y),
                                            Position(x + HEIGHT_ARROW, y - WIDTH_ARROW / 2 - WIDTH_ARROW_2))
        self.x_F, self.y_F = self._rotation(angle, Position(x, y), Position(x + HEIGHT_ARROW + HEIGHT_ARROW_2, y))
        self.x_G, self.y_G = self._rotation(angle, Position(x, y),
                                            Position(x + HEIGHT_ARROW, y + WIDTH_ARROW / 2 + WIDTH_ARROW_2))

    def clear(self):
        self.draw(BACKGROUND)

    def draw(self, color):
        # self._draw(BLACK)
        pygame.draw.polygon(self.interface.fenetre, color,
                            ((self.x_A, self.y_A),  # A
                             (self.x_B, self.y_B),  # B
                             (self.x_D, self.y_D),  # D
                             (self.x_G, self.y_G),  # G
                             (self.x_F, self.y_F),  # F
                             (self.x_E, self.y_E),  # E
                             (self.x_C, self.y_C)))  # C

class Personnage:
    def __init__(self, interface, img_path, position = Position(0,0)):
        self.interface = interface
        self.img = pygame.image.load(img_path).convert_alpha()
        self.position = Position(0,0)
        self.set_position(position)
        self.fleche = Fleche(interface)

    def set_position(self, position):
        self.position.x = position.x - self.img.get_width() / 2
        self.position.y = position.y - self.img.get_height() / 2

    def clear(self):
        pygame.draw.rect(self.interface.fenetre, BACKGROUND,
                         (self.position.x, self.position.y, self.img.get_width(), self.img.get_height()))

    def draw(self):
        self.interface.fenetre.blit(self.img, (self.position.x,
                                   self.position.y))


class Interface:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50, 5)
        self.dimensions = Dimensions(50,50)
        self.fenetre = pygame.display.set_mode((self.dimensions.width, self.dimensions.height))
        self.fenetre.fill(BACKGROUND)
        self.perso = Personnage(self, "img/perso1.png")
        self.enemis = {}
        self.position_souris = Position(0, 0)
        pygame.display.flip()

    def clear_enemis(self):
        [e.clear() for e in self.enemis.values()]

    def draw_enemis(self):
        [e.draw() for e in self.enemis.values()]

    def add_enemi(self, enemi):
        self.enemis[enemi.addr] = Personnage(self, "img/perso2.png", enemi.position)
        self.enemis[enemi.addr].draw()
        pygame.display.flip()

    def update_enemi(self, enemi):
        self.perso.clear()
        self.perso.fleche.clear()
        self.enemis[enemi.addr].clear()
        self.enemis[enemi.addr].set_position(enemi.position)
        self.enemis[enemi.addr].draw()
        self.perso.fleche.draw(BLACK)
        self.perso.draw()
        pygame.display.flip()


    def update_dimensions(self, dimensions):
        self.fenetre = pygame.display.set_mode((dimensions.width, dimensions.height))
        self.fenetre.fill(BACKGROUND)
        self.perso.fleche.draw(BLACK)
        self.perso.draw()
        pygame.display.flip()

    def update_position_souris(self, position_souris):
        self.perso.fleche.clear()
        self.perso.clear()
        self.clear_enemis()
        self.position_souris = position_souris
        self.perso.fleche.update()
        self.draw_enemis()
        self.perso.fleche.draw(BLACK)
        self.perso.draw()
        pygame.display.flip()


    def update_position(self, position):
        self.perso.clear()
        self.perso.fleche.clear()
        self.clear_enemis()
        self.perso.set_position(position)
        self.perso.fleche.update()
        self.draw_enemis()
        self.perso.fleche.draw(BLACK)
        self.perso.draw()
        pygame.display.flip()




