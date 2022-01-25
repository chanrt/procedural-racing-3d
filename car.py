import numpy as np
import pygame as pg
from math import sin, cos


def collide_with_walls(walls, current_x, current_y, future_x, future_y):
    x1, y1, x2, y2 = current_x, current_y, future_x, future_y

    for wall in walls:
        x3, y3, x4, y4 = wall.x3, wall.y3, wall.x4, wall.y4
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if denominator != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denominator
            if 0 < t < 1 and 0 < u < 1:
                return True
    return False


class Car:
    def __init__(self, x, y, look_angle, screen_width, screen_height):
        self.x = x
        self.y = y
        self.look_angle = np.deg2rad(look_angle)

        car_width = screen_width / 3
        car_height = screen_height / 4
        self.image = pg.transform.smoothscale(
            pg.image.load("car.png"), (car_width, car_height))

        self.screen_x = screen_width / 2 - car_width / 2
        self.screen_y = 5 * screen_height / 6 - car_height / 2

        self.speed = 0
        self.top_speed = 30
        self.reverse_speed = 5
        self.accelertion = 1
        self.deceleration = 0.2
        self.braking = 3

        self.turn_speed = np.deg2rad(1)

        self.front_distance = 300
        self.side_distance = 32

        self.collide_front = False
        self.collide_back = False
        self.collide_left = False
        self.collide_right = False

    def update(self, up_press, down_press, left_press, right_press, walls):

        print(self.collide_front, self.collide_back, self.collide_left, self.collide_right)

        if up_press and not self.collide_front:
            self.speed += self.accelertion
            if self.speed > self.top_speed:
                self.speed = self.top_speed
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
        if down_press:
            if self.speed == 0 and not self.collide_back:
                self.x -= self.reverse_speed * cos(self.look_angle)
                self.y -= self.reverse_speed * sin(self.look_angle)
            elif self.speed > 0 and not self.collide_front:
                self.speed -= self.braking
                if self.speed < 0:
                    self.speed = 0
                self.x += self.speed * cos(self.look_angle)
                self.y += self.speed * sin(self.look_angle)
        if left_press:
            if self.speed > 0 and not self.collide_front and not self.collide_left:
                self.look_angle -= self.turn_speed * self.speed / self.top_speed
            elif self.speed == 0 and down_press and not self.collide_back and not self.collide_right:
                self.look_angle += self.turn_speed
        if right_press:
            if self.speed > 0 and not self.collide_front and not self.collide_right:
                self.look_angle += self.turn_speed * self.speed / self.top_speed
            elif self.speed == 0 and down_press and not self.collide_back and not self.collide_left:
                self.look_angle -= self.turn_speed
        if not up_press and not down_press and self.speed > 0 and not self.collide_front and not self.collide_left and not self.collide_right:
            self.speed -= self.deceleration
            if self.speed < 0:
                self.speed = 0
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance + self.speed + self.accelertion) * cos(self.look_angle),
            self.y + (self.front_distance + self.speed + self.accelertion) * sin(self.look_angle)
        ):
            self.collide_front = True
            self.speed = 0
        else:
            self.collide_front = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance - self.reverse_speed) * cos(self.look_angle),
            self.y + (self.front_distance - self.reverse_speed) * sin(self.look_angle)
        ):
            self.collide_back = True
        else:
            self.collide_back = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance * cos(self.look_angle) + self.side_distance * cos(self.look_angle - np.pi / 2),
            self.y + self.front_distance * sin(self.look_angle) + self.side_distance * sin(self.look_angle - np.pi / 2)
        ):
            self.collide_left = True
        else:
            self.collide_left = False
        
        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance * cos(self.look_angle) + self.side_distance * cos(self.look_angle + np.pi / 2),
            self.y + self.front_distance * sin(self.look_angle) + self.side_distance * sin(self.look_angle + np.pi / 2)
        ):
            self.collide_right = True
        else:
            self.collide_right = False

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))
