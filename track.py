from math import sin, cos, fabs
from wall import Wall
import random
from matplotlib import pyplot as plt
import numpy as np


class Track:
    def __init__(self, max_distance, road_width):
        self.max_distance = max_distance
        self.road_width = road_width

        self.wall_segment_length = 2000
        self.front_load_distance = 8000
        self.back_load_distance = 4000

        self.plot_track = False

        self.track_curvature = []
        self.walls = []

        self.current_angle = 0
        self.current_distance = 0

        self.build_bluprint()
        self.build_track()

    def build_bluprint(self):
        self.track_curvature = []

        any_direction = [
            self.straight_track, self.straight_track,
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.sharp_right_turn,
            self.tight_left_turn, self.tight_right_turn
        ]
        left_direction = [
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.tight_left_turn
        ]
        right_direction = [
            self.gradual_right_turn, self.gradual_left_turn,
            self.sharp_right_turn, self.tight_right_turn
        ]

        while self.current_distance < self.max_distance:
            if fabs(self.current_angle) < np.pi / 4:
                next_section = random.choice(any_direction)
                next_section()
            elif self.current_angle <= -np.pi / 4:
                next_section = random.choice(right_direction)
                next_section()
            elif self.current_angle >= np.pi / 4:
                next_section = random.choice(left_direction)
                next_section()

    def straight_track(self):
        self.track_curvature += [0 for _ in range(random.randint(2, 4))]

    def gradual_left_turn(self):
        self.track_curvature += [-0.1, -0.1, -0.1, -0.1, -0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle -= 0.5

    def gradual_right_turn(self):
        self.track_curvature += [0.1, 0.1, 0.1, 0.1, 0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle += 0.5

    def sharp_left_turn(self):
        self.track_curvature += [-0.3, -0.3, -0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle -= 0.9

    def sharp_right_turn(self):
        self.track_curvature += [0.3, 0.3, 0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle += 0.9

    def tight_left_turn(self):
        self.track_curvature += [-0.2, -0.2, -0.2, -0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle -= 0.8

    def tight_right_turn(self):
        self.track_curvature += [0.2, 0.2, 0.2, 0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle += 0.8

    def smooth_hairpin(self):
        if random() > 0.5:
            self.gradual_left_turn()
            self.gradual_right_turn()
        else:
            self.gradual_right_turn()
            self.gradual_left_turn()

    def build_track(self):
        self.walls.append(Wall(0, 0, 0, self.road_width))
        self.walls.append(Wall(0, 0, self.wall_segment_length, 0))
        self.walls.append(
            Wall(0, self.road_width, self.wall_segment_length, self.road_width))

        self.current_angle = 0
        for angle in self.track_curvature:
            self.current_angle += angle
            x3 = self.walls[-2].x4
            y3 = self.walls[-2].y4
            x4 = x3 + self.wall_segment_length * cos(self.current_angle)
            y4 = y3 + self.wall_segment_length * sin(self.current_angle)
            self.walls.append(Wall(x3, y3, x4, y4))

            horizontal_width = self.road_width * \
                sin(self.current_angle + np.pi / 2)
            vertical_width = self.road_width * \
                cos(self.current_angle + np.pi / 2)
            self.walls.append(Wall(
                self.walls[-2].x4, self.walls[-2].y4, x4 + vertical_width, y4 + horizontal_width))

        self.final_x = self.walls[-1].x4

        if self.plot_track:
            x, y = [], []
            for i, wall in enumerate(self.walls):
                if i % 2 == 1:
                    x.append(wall.x3)
                    y.append(wall.y3)
            plt.plot(x, y)

            x, y = [], []
            for i, wall in enumerate(self.walls):
                if i % 2 == 0:
                    x.append(wall.x3)
                    y.append(wall.y3)
            plt.plot(x, y)
            plt.show()

    def load_walls(self, car_position):
        visible_walls = []

        for wall in self.walls:
            if -self.back_load_distance < wall.x3 - car_position < self.front_load_distance:
                visible_walls.append(wall)
        return visible_walls
