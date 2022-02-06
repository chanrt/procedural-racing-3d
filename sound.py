import pygame as pg
from time import sleep
from loader import get_resource_path

class Sound:
    def __init__(self):
        self.state = "starting"
        
        pg.mixer.init()
        
        self.idle_sound = pg.mixer.Sound(get_resource_path("sounds/idle.mp3"))
        self.brake_sound = pg.mixer.Sound(get_resource_path("sounds/brake.mp3"))
        self.top_sound = pg.mixer.Sound(get_resource_path("sounds/top_speed.mp3"))
        
        self.crash_sound = pg.mixer.Sound(get_resource_path("sounds/crash.mp3"))
        self.scratch_sound = pg.mixer.Sound(get_resource_path("sounds/scratch.wav"))
        self.finish_sound = pg.mixer.Sound(get_resource_path("sounds/finish.wav"))

    def stop_sound(self):
        try:
            if self.state == "idle":
                self.idle_sound.stop()
            elif self.state == "accelerate" or self.state == "decelerate":
                pg.mixer.music.stop()
            elif self.state == "top":
                self.top_sound.stop()
            elif self.state == "brake":
                self.brake_sound.stop()
            elif self.state == "crash":
                self.crash_sound.stop()
            pg.mixer.pause()
        except:
            pass

    def play_idle(self):
        state_changed = False

        if self.state == "starting":
            state_changed = True
        elif self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "crash":
            self.state_change = True

        if state_changed:
            self.state = "idle"
            self.idle_sound.play(100000)

    def play_accelerate(self, position):
        state_changed = False

        if self.state == "idle":
            self.idle_sound.stop()
            state_changed = True
        elif self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "crash":
            state_changed = True

        if state_changed:
            self.state = "accelerate"
            pg.mixer.music.load(get_resource_path("sounds/accelerate.mp3"))
            pg.mixer.music.play(0, position * 10)

    def stop_accelerate(self):
        if self.state == "accelerate":
            pg.mixer.music.stop()

    def play_decelerate(self, position):
        state_changed = False

        if self.state == "accelerate":
            pg.mixer.music.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "top":
            self.top_sound.stop()
            state_changed = True

        if state_changed:
            self.state = "decelerate"
            pg.mixer.music.load(get_resource_path("sounds/decelerate.mp3"))
            pg.mixer.music.play(0, position * 10)

    def play_brake(self):
        state_changed = False

        if self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        if self.state == "top":
            self.top_sound.stop()
            state_changed = True

        if state_changed:
            self.state = "brake"
            self.brake_sound.play()

    def play_top(self):
        state_changed = False

        if self.state == "accelerate":
            pg.mixer.music.stop()
            state_changed = True

        if state_changed:
            self.state = "top"
            self.top_sound.play(100000)

    def play_crash(self):
        state_changed = False

        if self.state == "idle":
            self.idle_sound.stop()
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "top":
            self.top_sound.stop()
            state_changed = True
        elif self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True

        if state_changed:
            self.state = "crash"
            self.crash_sound.play()

    def play_scratch(self):
        pass

    def play_finish(self):
        pg.mixer.music.stop()
        if self.state == "idle":
            self.idle_sound.stop()
        elif self.state == "brake":
            self.brake_sound.stop()
        elif self.state == "top":
            self.top_sound.stop()            

        self.finish_sound.play()
        sleep(1)