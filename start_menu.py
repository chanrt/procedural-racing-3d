import pygame as pg
from loader import get_resource_path

def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0] 
    max_width, _ = surface.get_size()
    max_width = max_width / 2

    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0] 
        y += word_height

def start_menu():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Procedural Racing 3D")
    clock = pg.time.Clock()
    title_font = pg.font.SysFont(None, 48)
    text_font = pg.font.SysFont(None, 36)

    bg_color = pg.Color(48, 48, 48)
    font_color = pg.Color("white")

    title_text = title_font.render("Procedural Racing 3D", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    left_text =  "CONTROLS:\n\
Use WASD or Cursor keys for steering the car\n\
Press R to restart the current track\n\
Press Escape to quit\n\n\n\
IMPORTANT:\n\
If unresponsive, click on the game window\n\
Also, collision detection is a bit buggy\n\n\n\
ABOUT:\n\
Developed by ChanRT | Fork me at GitHub"

    button_1 = pg.image.load(get_resource_path("buttons/button_1.png"))
    button_2 = pg.image.load(get_resource_path("buttons/button_2.png"))
    button_3 = pg.image.load(get_resource_path("buttons/button_3.png"))
    button_4 = pg.image.load(get_resource_path("buttons/button_4.png"))

    running = True
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                if 500 < mouse_x < 700:
                    if 100 < mouse_y < 200:
                        return 5
                    elif 225 < mouse_y < 325:
                        return 10
                    elif 350 < mouse_y < 450:
                        return 15
                    elif 475 < mouse_y < 575:
                        return 20

        screen.fill(bg_color)

        screen.blit(title_text, title_rect)
        blit_text(screen, left_text, (10, 100), text_font, font_color)

        screen.blit(button_1, (500, 100))
        screen.blit(button_2, (500, 225))
        screen.blit(button_3, (500, 350))
        screen.blit(button_4, (500, 475))

        pg.display.flip()
    pg.quit()
    return None