import pygame as pg

class Progress:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.width = screen_width / 30
        self.height = screen_height / 2

        self.image = pg.transform.smoothscale(pg.image.load("sprites/checkerboard.png"), (self.width, self.height / 10)).convert()

        self.x = screen_width - 3 * self.width / 2
        self.y = (screen_height - self.height) / 2

        self.outer_rect = pg.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
        self.outer_color = pg.Color(32, 32, 32)
        self.inner_color = pg.Color("#1f51ff")

    def render(self, screen):
        length = (self.car.x / self.track.final_x) * self.height
        inner_rect = pg.Rect(self.x, self.y + self.height - length, self.width, length)
        pg.draw.rect(screen, self.outer_color, self.outer_rect)
        pg.draw.rect(screen, self.inner_color, inner_rect)
        screen.blit(self.image, (self.x, self.y))