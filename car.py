import numpy as np
import pygame as pg
from math import sin, cos, fabs
from sound import Sound
from loader import get_resource_path

def collide_with_walls(walls, current_x, current_y, future_x, future_y):
    for wall in walls:
        if fabs(current_x - wall.x3) < 3000:
            denominator = (current_x - future_x) * (wall.y3 - wall.y4) - \
                (current_y - future_y) * (wall.x3 - wall.x4)

            if denominator != 0:
                t = ((current_x - wall.x3) * (wall.y3 - wall.y4) -
                     (current_y - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((current_x - wall.x3) * (current_y - future_y) -
                     (current_y - wall.y3) * (current_x - future_x)) / denominator
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
            pg.image.load(get_resource_path("sprites/car.png")), (car_width, car_height)).convert_alpha()

        self.screen_x = screen_width / 2 - car_width / 2
        self.screen_y = 5 * screen_height / 6 - car_height / 2

        self.speed = 0
        self.top_speed = 100
        self.reverse_speed = 5
        self.acceleration = 0.5

        self.deceleration = 0.33
        self.braking = 3

        self.turn_speed = np.deg2rad(1)

        self.front_distance = 300
        self.side_distance = 32

        self.collide_front = False
        self.collide_back = False
        self.collide_left = False
        self.collide_right = False

        self.wall_behind = False
        self.collide_x = 0
        self.collide_y = 0

        self.sound = Sound()

    def update(self, up_press, down_press, left_press, right_press, walls):
        if self.speed <= 0:
            self.sound.play_idle()
        if self.speed == self.top_speed:
            self.sound.play_top()
            
        if up_press and not self.collide_front:
            self.speed += self.acceleration
            if self.speed > self.top_speed:
                self.speed = self.top_speed
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
            self.sound.play_accelerate(self.speed / self.top_speed)
        if down_press:
            if self.speed == 0 and not self.collide_back:
                self.x -= self.reverse_speed * cos(self.look_angle)
                self.y -= self.reverse_speed * sin(self.look_angle)
            elif self.speed > 0 and not self.collide_front:
                self.sound.play_brake()
                self.speed -= self.braking
                if self.speed < 0:
                    self.speed = 0
                self.x += self.speed * cos(self.look_angle)
                self.y += self.speed * sin(self.look_angle)
        if left_press:
            if self.speed > 0 and not self.collide_front and not self.collide_left:
                self.look_angle -= self.turn_speed * (1.5 - self.speed / self.top_speed)
            elif self.speed == 0 and down_press and not self.collide_back and not self.collide_right:
                self.look_angle += self.turn_speed
        if right_press:
            if self.speed > 0 and not self.collide_front and not self.collide_right:
                self.look_angle += self.turn_speed * (1.5 - self.speed / self.top_speed)
            elif self.speed == 0 and down_press and not self.collide_back and not self.collide_left:
                self.look_angle -= self.turn_speed
        if not up_press and not down_press and self.speed > 0 and not self.collide_front and not self.collide_left and not self.collide_right:
            self.sound.play_decelerate(1 - self.speed / self.top_speed)
            if self.speed / self.top_speed > 0.66:
                self.speed -= 3 * self.deceleration
            elif self.speed / self.top_speed > 0.33:
                self.speed -= 2 * self.deceleration
            self.speed -= self.deceleration
            if self.speed < 0:
                self.speed = 0
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance + self.speed + self.acceleration) * cos(self.look_angle),
            self.y + (self.front_distance + self.speed + self.acceleration) * sin(self.look_angle)
        ):
            self.collide_front = True
            self.sound.play_crash()
            self.collide_speed = self.speed
            self.speed = 0

            self.collide_x = self.x + self.front_distance * cos(self.look_angle)
            self.collide_y = self.y + self.front_distance * sin(self.look_angle)
        else:
            if self.x + self.front_distance * cos(self.look_angle) != self.collide_x or self.y + self.front_distance * sin(self.look_angle) != self.collide_y:
                self.collide_front = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance - self.reverse_speed) *
            cos(self.look_angle),
            self.y + (self.front_distance - self.reverse_speed) *
            sin(self.look_angle)
        ):
            self.collide_back = True
            self.sound.play_crash()
        else:
            self.collide_back = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle - np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle - np.pi / 2)
        ):
            self.sound.play_scratch()
            self.collide_left = True
        else:
            self.collide_left = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle + np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle + np.pi / 2)
        ):
            self.sound.play_scratch()
            self.collide_right = True
        else:
            self.collide_right = False

        if collide_with_walls(
            walls,
            self.x,
            self.y,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle)
        ):
            self.wall_behind = True
        else:
            self.wall_behind = False

        if self.x < 0:
            self.x = 0  

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.look_angle = 0
