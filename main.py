import start_menu #파일 이름임
import real_game #파일 이름임
import pygame

pygame.init()
condition = "start_menu"

running = True
reseted = False

while (running == True):
    match (condition):
        case "start_menu":
            condition = start_menu.run()
        case "real_game":
            results = real_game.run(reseted)
            condition = results[0]
            reseted = results[1]
        case "quit":
            running = False

pygame.quit()