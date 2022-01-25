from math import fabs, ceil, sqrt
import pygame as pg

class Wall:
    def __init__(self, x3, y3, x4, y4):
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.total = sqrt(x3 * x3 + x4 * x4)

        self.color = pg.Color("blue")
        self.width = 5

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x3, self.y3), (self.x4, self.y4), self.width)