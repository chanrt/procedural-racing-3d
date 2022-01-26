import pygame as pg

class Progress:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.width = screen_width / 25
        self.height = 2 * screen_height / 3

        self.x = self.width / 2
        self.y = (screen_height - self.height) / 2

        self.outer_rect = pg.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
        self.outer_color = pg.Color(32, 32, 32)
        self.inner_color = pg.Color("#1f51ff")

    def render(self, screen):
        length = (self.car.x / self.track.final_x) * self.height
        inner_rect = pg.Rect(self.x, self.y + self.height - length, self.width, length)
        pg.draw.rect(screen, self.outer_color, self.outer_rect)
        pg.draw.rect(screen, self.inner_color, inner_rect)