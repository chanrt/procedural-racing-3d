from math import sin, cos, pow, sqrt
import pygame as pg

class Ray:
    def __init__(self, angle):
        self.angle = angle
        self.color = pg.Color("yellow")
        self.width = 1

    def cast(self, position, walls):
        self.x1 = position[0]
        self.y1 = position[1]
        self.x2 = self.x1 + cos(self.angle)
        self.y2 = self.y1 + sin(self.angle)

        min_distance = 10e8
        self.texture = 0

        for wall in walls:
            denominator = (self.x1 - self.x2) * (wall.y3 - wall.y4) - (self.y1 - self.y2) * (wall.x3 - wall.x4)
            if denominator == 0:
                t, u = 0, 0
            else:
                t = ((self.x1 - wall.x3) * (wall.y3 - wall.y4) - (self.y1 - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((self.x1 - wall.x3) * (self.y1 - self.y2) - (self.y1 - wall.y3) * (self.x1 - self.x2)) / denominator

            if t > 0 and 0 < u < 1: 
                x2 = self.x1 + t * (self.x2 - self.x1)
                y2 = self.y1 + t * (self.y2 - self.y1)
                distance = pow(x2 - self.x1, 2) + pow(y2 - self.y1, 2)

                if distance < min_distance:
                    self.texture = (u // 0.001) % 100
                    min_distance = distance
                    self.x2 = x2
                    self.y2 = y2

        return sqrt(min_distance)

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)