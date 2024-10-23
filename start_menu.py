import pygame
from pygame.locals import *
import os
import button
import real_game
import map_loading

pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
running = True
script_dir = os.path.dirname(__file__)

start_button = button.button(screen_width/2-181,600,"시작1.png","시작2.png")
def run():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"

    screen.blit(pygame.image.load(f"{script_dir}//images//시작배경.png"),(0,0))
    if start_button.button_work() == True:
        result = "real_game"
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    else:
        result = "start_menu"
    pygame.display.update()
    return result