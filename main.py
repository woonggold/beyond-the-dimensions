import start_menu #파일 이름임
import real_game #파일 이름임

condition = "start_menu"

while (running == True):
    match (condition):
        case "start_menu":
            condition = start_menu.run()
        case "real_game":
            condition = real_game.run()
        case "quit":
            running = False