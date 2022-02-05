import time
from car import Car
from ray import Ray
from loader import get_resource_path
from minimap import Minimap
from progress import Progress
from speedometer import Speedometer
from start_menu import start_menu
from track import Track
import numpy as np
import pygame as pg

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def generate_rays(look_angle, fov, screen_width, res):
    return [Ray(angle) for angle in np.arange(look_angle - fov / 2, look_angle + fov / 2, fov * res / screen_width)]

def play_game(track_distance):

    # initialize pygame
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Procedural Racing 3D")
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)

    # critical settings
    fov = np.deg2rad(60)
    height_scale = 100000
    shader_exponent = 2
    res = 1
    fps = 48
    road_width = 400

    # static elements
    bg_color = pg.Color(21, 1, 3)
    font_color = pg.Color("white")
    road_color = pg.Color(48, 48, 48)
    road_rect = pg.Rect(0, screen_height / 2, screen_width, screen_height / 2)
    title_text = font.render("Procedural Racing 3D", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    # load objects
    car = Car(0, road_width / 2, 0, screen_width, screen_height)
    speedometer = Speedometer(car, screen_width, screen_height)
    track = Track(track_distance * 20000, road_width)
    rays = generate_rays(car.look_angle, fov, screen_width, res)
    walls = track.load_walls(car.x)
    progress_bar = Progress(car, track, screen_width, screen_height)
    minimap = Minimap(car, track, screen_width, screen_height)
    skyline = pg.transform.smoothscale(pg.image.load(get_resource_path("sprites/skyline.jpg")), (screen_width, screen_height / 2)).convert()
    skyline_turn_sensitivity = 200

    # dynamic loader of walls
    load_walls = pg.USEREVENT + 1
    pg.time.set_timer(load_walls, 1000)

    # timers and controls
    race_timer = None
    timer_started = False
    up_press, down_press, left_press, right_press = False, False, False, False

    running = True
    # main loop
    while running:
        clock.tick(fps)

        # initial rendering
        screen.fill(bg_color)
        skyline_x = -skyline_turn_sensitivity * car.look_angle
        screen.blit(skyline, (skyline_x, 0))
        if skyline_x > 0:
            screen.blit(skyline, (skyline_x - screen_width, 0))
        elif skyline_x < 0:
            screen.blit(skyline, (skyline_x + screen_width, 0))
        pg.draw.rect(screen, road_color, road_rect)

        # checking for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_program()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    car.sound.stop_sound()
                    running = False
                if event.key == pg.K_UP or event.key == pg.K_w:
                    up_press = True
                    if not timer_started:
                        race_timer = time.time()
                        timer_started = True
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    down_press = True
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    left_press = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    right_press = True
                if event.key == pg.K_r:
                    # restart track
                    car.reset(0, road_width / 2)
                    timer_started = False
                    walls = track.load_walls(car.x)
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    up_press = False
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    down_press = False
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    left_press = False
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    right_press = False
            if event.type == load_walls:
                walls = track.load_walls(car.x)

                if clock.get_fps() < 24:
                    # automatically lower graphics if fps is low
                    res += 1
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
                    print(f"Decreased anti-aliasing to {100 - 10 * res}% to increase performance")

        # car dynamics
        car.update(up_press, down_press, left_press, right_press, walls)

        # check if race finished
        if car.x > track.final_x:
            car.sound.play_finish()
            pg.quit()
            running = False
            return (time.time() - race_timer)
        
        # ray casting
        if (left_press or right_press) and (car.speed > 0 or down_press):
            rays = generate_rays(car.look_angle, fov, screen_width, res)

        distances = np.zeros(len(rays), float)
        for i, ray in enumerate(rays):
            distances[i] = ray.cast((car.x, car.y), walls)

        # rendering walls
        for x, distance in enumerate(distances):
            height = height_scale / distance
            if height > screen_height:
                height = screen_height
            texture = translate(rays[x].texture * 2, 0, 200, 32, 64)
            raw_color = translate(height ** shader_exponent, 0, screen_height ** shader_exponent, 100, 200)
            pg.draw.line(screen, [raw_color, texture, 0], (x * res, (screen_height - height) / 2), (x * res, (screen_height + height) / 2), res)
        
        # rendering car
        if not car.wall_behind:
            car.render(screen)

        # rendering UI elements 
        speedometer.render(screen)
        progress_bar.render(screen)
        minimap.render(screen)

        # rendering text
        fps_display = font.render("FPS: " + str(int(clock.get_fps())), True, font_color)
        screen.blit(fps_display, (0, 0))
        screen.blit(title_text, title_rect)

        if timer_started:
            time_display = font.render(str(round(time.time() - race_timer, 2)), True, font_color)
            screen.blit(time_display, (screen_width - 100, 0))
        
        pg.display.flip()

def exit_program():
    pg.quit()
    quit()

if __name__ == "__main__":

    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass

    while True:
        length = start_menu()
        if length == 0 or length is None:
            break
        play_game(length)