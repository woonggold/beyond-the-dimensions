import start_menu

condition = "start_menu"

running = True
reseted = False

while (running == True):
    match (condition): 
        case "start_menu":
            condition = start_menu.run()
        case "quit":
            running = False