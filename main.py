import start_menu #파일 이름임
import real_game #파일 이름임
import ending #파일 이름임
import pygame
import start_video

condition = "real_game"

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
