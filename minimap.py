from math import sin, cos
import pygame as pg

class Minimap:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.radius = screen_width / 12
        self.x = 3 * self.radius / 2
        self.y = screen_height - 3 * self.radius / 2

        self.road_length = self.radius / 6
        self.car_rect = pg.Rect(self.x - 4, self.y - 4, 8, 8)

        self.background_color = pg.Color("black")
        self.road_color = pg.Color(128, 128, 128)
        self.player_color = pg.Color("red")

    def get_position(self):
        for i in range(0, len(self.track.walls), 2):
            if self.track.walls[i].x3 < self.car.x < self.track.walls[i].x4:
                return i
        return 0

    def render(self, screen):
        pg.draw.circle(screen, self.background_color, (self.x, self.y), self.radius)

        car_position = self.get_position()

        # obtain track around car
        track_angles = []
        for offset in range(-10, 12, 2):
            track_position = int((car_position + offset) / 2)
            if 0 < track_position < len(self.track.track_curvature):
                track_angles.append(self.track.track_curvature[track_position])
            else:
                track_angles.append(None)

        front_x, front_y = self.x, self.y - self.road_length / 2
        back_x, back_y = self.x, self.y + self.road_length / 2
        pg.draw.line(screen, self.road_color, (front_x, front_y), (back_x, back_y), 3)

        current_x, current_y = front_x, front_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track in front of car
        for i in range(6, 11):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y - self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle
        
        current_x, current_y = back_x, back_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track behind car
        for i in range(4, -1, -1):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y + self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle

        pg.draw.rect(screen, self.player_color, self.car_rect)