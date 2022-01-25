import time
from car import Car
from ray import Ray
from wall import Wall
import numpy as np
import pygame as pg

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

def generate_rays(look_angle, fov, screen_width):
    return [Ray(angle) for angle in np.arange(look_angle - fov / 2, look_angle + fov / 2, fov / screen_width)]

def loop():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("3D Raycaster for oblique, textured walls")
    pg.mouse.set_visible(False)

    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)

    bg_color = pg.Color(32, 32, 32)
    ceiling_color = pg.Color("blue")
    font_color = pg.Color("black")
    floor_color = pg.Color(32, 32, 32)
    floor_rect = pg.Rect(0, screen_height / 2, screen_width, screen_height / 2)

    walls = []
    walls.append(Wall(0, 0, 10000, 0))
    walls.append(Wall(0, 400, 10000, 400))

    car = Car(0, 200, 0, screen_width, screen_height)

    fov = np.deg2rad(60)
    height_scale = 100000
    shader_exponent = 0.9

    rays = generate_rays(car.look_angle, fov, screen_width)

    show_walls = False
    up_press, down_press, left_press, right_press = False, False, False, False

    while 1:
        clock.tick(60)
        
        if show_walls:
            screen.fill(bg_color)
        else:
            screen.fill(ceiling_color)
            pg.draw.rect(screen, floor_color, floor_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_program()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit_program()
                if event.key == pg.K_TAB:
                    show_walls = not show_walls
                if event.key == pg.K_UP:
                    up_press = True
                if event.key == pg.K_DOWN:
                    down_press = True
                if event.key == pg.K_LEFT:
                    left_press = True
                if event.key == pg.K_RIGHT:
                    right_press = True
                if event.key == pg.K_r:
                    car.x = 0
                    car.y = 200
                    car.look_angle = 0
                    car.speed = 0
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    up_press = False
                if event.key == pg.K_DOWN:
                    down_press = False
                if event.key == pg.K_LEFT:
                    left_press = False
                if event.key == pg.K_RIGHT:
                    right_press = False

        car.update(up_press, down_press, left_press, right_press, walls)

        if (left_press or right_press) and (car.speed > 0 or down_press):
            rays = generate_rays(car.look_angle, fov, screen_width)

        distances = np.zeros(len(rays), float)
        for i, ray in enumerate(rays):
            distances[i] = ray.cast((car.x, car.y), walls)

        if show_walls:
            for wall in walls:
                wall.render(screen)
            for ray in rays:
                ray.render(screen)
        else:
            for x, distance in enumerate(distances):
                height = height_scale / distance
                if height > screen_height:
                    height = screen_height
                texture = translate(rays[x].texture * 2, 0, 200, 32, 64)
                raw_color = translate(height ** shader_exponent, 0, screen_height ** shader_exponent, 100, 200)
                pg.draw.line(screen, [raw_color, texture, 0], (x, (screen_height - height) / 2), (x, (screen_height + height) / 2))

        car.render(screen)

        fps_display = font.render(str(int(clock.get_fps())), True, font_color)
        screen.blit(fps_display, (0, 0))
        pg.display.flip()

def exit_program():
    pg.quit()
    quit()

if __name__ == "__main__":
    loop()