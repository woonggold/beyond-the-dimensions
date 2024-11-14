import start_menu
import real_game
import ending
import pygame
import start_video

condition = "real_game"
import map_loading
map_loading.map_load("stage6")

running = True
reseted = False

while (running == True):
    match (condition): 
        case "start_menu":
            condition = start_menu.run()
        case "start_video":
            condition = start_video.run()
        case "real_game":
            condition = real_game.run()
        case "ending":
            condition = ending.run()
        case "quit":
            running = False
            

pygame.quit()
