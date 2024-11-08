import start_menu #파일 이름임
import real_game #파일 이름임
import pygame
from settings import *

pygame.init()
condition = "start_menu"

running = True
reseted = False

while (running == True):
    match (condition): 
        case "start_menu":
            condition = start_menu.run()
        case "real_game":
            condition = real_game.run()
        case "quit":
            running = False

pygame.quit()
