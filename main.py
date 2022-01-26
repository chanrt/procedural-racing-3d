import time
from car import Car
from ray import Ray
from progress import Progress
from speedometer import Speedometer
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
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    road_width = 400

    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("3D Raycaster for oblique, textured walls")

    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)

    bg_color = pg.Color(21, 1, 3)
    font_color = pg.Color("white")
    road_color = pg.Color(48, 48, 48)
    road_rect = pg.Rect(0, screen_height / 2, screen_width, screen_height / 2)

    car = Car(0, road_width / 2, 0, screen_width, screen_height)
    speedometer = Speedometer(car, screen_width, screen_height)
    track = Track(track_distance * 20000, road_width)
    walls = track.load_walls(car.x)

    progress_bar = Progress(car, track, screen_width, screen_height)

    skyline = pg.transform.smoothscale(pg.image.load("sprites/skyline.jpg"), (screen_width, screen_height / 2)).convert()
    skyline_turn_sensitivity = 200

    fov = np.deg2rad(60)
    height_scale = 100000
    shader_exponent = 2

    res = 1

    rays = generate_rays(car.look_angle, fov, screen_width, res)
    up_press, down_press, left_press, right_press = False, False, False, False

    load_walls = pg.USEREVENT + 1
    pg.time.set_timer(load_walls, 1000)

    frame_counter = 0

    race_timer = None
    timer_started = False

    while 1:
        clock.tick(48)

        start = time.time()
        screen.fill(bg_color)

        skyline_x = -skyline_turn_sensitivity * car.look_angle
        screen.blit(skyline, (skyline_x, 0))

        if skyline_x > 0:
            screen.blit(skyline, (skyline_x - screen_width, 0))
        elif skyline_x < 0:
            screen.blit(skyline, (skyline_x + screen_width, 0))
        pg.draw.rect(screen, road_color, road_rect)
        # print("Initial rendering:", time.time() - start)

        start = time.time()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_program()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit_program()
                if event.key == pg.K_UP:
                    up_press = True
                    if not timer_started:
                        race_timer = time.time()
                        timer_started = True
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

                    timer_started = False
                    walls = track.load_walls(car.x)
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    up_press = False
                if event.key == pg.K_DOWN:
                    down_press = False
                if event.key == pg.K_LEFT:
                    left_press = False
                if event.key == pg.K_RIGHT:
                    right_press = False
            if event.type == load_walls:
                walls = track.load_walls(car.x)

                if clock.get_fps() < 24:
                    res += 1
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
                    print(f"Decreased anti-aliasing to {100 - 10 * res}% to increase performance")
        # print("Checking for events:", time.time() - start)

        start = time.time()
        car.update(up_press, down_press, left_press, right_press, walls)
        # print("Car dynamics:", time.time() - start)
        
        start = time.time()
        if (left_press or right_press) and (car.speed > 0 or down_press):
            rays = generate_rays(car.look_angle, fov, screen_width, res)

        distances = np.zeros(len(rays), float)
        for i, ray in enumerate(rays):
            distances[i] = ray.cast((car.x, car.y), walls)
        # print("Ray casting:", time.time() - start)

        start = time.time()
        for x, distance in enumerate(distances):
            height = height_scale / distance
            if height > screen_height:
                height = screen_height
            texture = translate(rays[x].texture * 2, 0, 200, 32, 64)
            raw_color = translate(height ** shader_exponent, 0, screen_height ** shader_exponent, 100, 200)
            pg.draw.line(screen, [raw_color, texture, 0], (x * res, (screen_height - height) / 2), (x * res, (screen_height + height) / 2), res)
        
        if not car.wall_behind:
            car.render(screen)
        speedometer.render(screen)
        progress_bar.render(screen)

        if car.x > track.final_x:
            pg.quit()
            return (time.time() - race_timer)

        fps_display = font.render("FPS: " + str(int(clock.get_fps())), True, font_color)
        screen.blit(fps_display, (0, 0))

        if timer_started:
            time_display = font.render(str(round(time.time() - race_timer, 2)), True, font_color)
            screen.blit(time_display, (screen_width - 100, 0))
        
        pg.display.flip()
        # print("Final rendering:", time.time() - start)

        frame_counter += 1

def exit_program():
    pg.quit()
    quit()

if __name__ == "__main__":
    print("---> Procedural Racing 3D <---\n")
    print("CONTROLS:")
    print("Use WASD or Cursor keys for steering the car")
    print("Press R to restart the current track")
    print("Press Escape to quit\n")
    print("IMPORTANT: If unresponsive, click on the game window\n")
    print("ABOUT: Developed by ChanRT | Fork me at GitHub\n")

    while 1:
        length = int(input("Enter track length (preferably between 1 and 20 km): "))
        time_taken = play_game(length)
        print(f"Race completed in {round(time_taken, 2)} seconds!\n")
    
        play_again = input("Would you like to play again? (y/n): ")
        if play_again == "y":
            continue
        elif play_again == "n":
            exit_program()
        else:
            exit_program()