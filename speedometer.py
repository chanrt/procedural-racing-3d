import pygame as pg
from math import sin, cos, pi
from loader import get_resource_path

class Speedometer:
    def __init__(self, car, screen_width, screen_height):
        self.car = car

        speedometer_width = screen_width / 4
        speedometer_height = screen_height / 4

        self.image = pg.transform.smoothscale(pg.image.load(
            get_resource_path("sprites/speedometer.png")), (speedometer_width, speedometer_height)).convert_alpha()

        self.screen_x = screen_width - (speedometer_width)
        self.screen_y = screen_height - (speedometer_height)

        self.needle_x = screen_width - (speedometer_width / 2)
        self.needle_y = screen_height - 20
        self.needle_length = speedometer_height / 1.7
        self.needle_color = pg.Color("#1f51ff")

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))

        angle = pi * self.car.speed / self.car.top_speed
        tip_x = self.needle_x - self.needle_length * cos(angle)
        tip_y = self.needle_y - self.needle_length * sin(angle)
        pg.draw.line(screen, self.needle_color, (self.needle_x, self.needle_y), (tip_x, tip_y), 3)