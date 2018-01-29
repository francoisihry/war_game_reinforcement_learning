# class Test:
#     def __init__(self):
#         self.a=33
#
# t = Test()
#
# t_d =pickle.dumps(t)
#
# t_l= pickle.loads(t_d)
# pass
# print("a={}".format(t_l.a))

UP = 0
UP_RIGHT = 40
UP_LEFT = 20

DOWN = 1
DOWN_RIGHT = 41
DOWN_LEFT = 21

LEFT = 2
RIGHT = 4


class Dimensions:
    def __init__(self, width, height):
        self.width,self.height = width,height

class Position:
    def __init__(self, x, y):
        self.x,self.y = x,y

class Enemi:
    def __init__(self, addr, position):
        self.addr = addr
        self.position = position


class Move:
    def __init__(self, dir):
        self.dir = dir

class Start:
    pass

class Tir:
    def __init__(self, vect_direction):
        self.vect_direction = vect_direction


class Quit:
    pass