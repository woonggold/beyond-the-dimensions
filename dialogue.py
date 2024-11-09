import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIALOGUE_BOX_COLOR = (50, 50, 50)

# Font
font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 36)
current_dialogue_index = 0
is_talking = False
first_talk = 0
second_talk = 0

#대화문{다른 파일로 옮길 예정}
talking = {
    "dialogues": [
        " 어어…",
        "왜 내가 천장에 있지…?",
        "..아",
        "내가 천장에 있는게 아니라",
        "세상이 뒤바뀐거구나..",
        "..젠장"
    ]
}


def talkcheck():
    import real_game
    global is_talking, current_dialogue_index, first_talk, second_talk
    if is_talking == True and (first_talk == 1 or second_talk == 1):
        real_game.prevent2 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


            if event.type == pygame.MOUSEBUTTONDOWN:  # 대화창 클릭
                current_dialogue_index += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:  # 스페이스 키로 대화 넘기기
                    current_dialogue_index += 1
                if event.key == pygame.K_a:
                    real_game.player.dx -= real_game.player.speed

                if event.key == pygame.K_d:
                    real_game.player.dx += real_game.player.speed

                if event.key == pygame.K_w:#z축 앞 이동
                    real_game.player.dz += real_game.player.speed

                if event.key == pygame.K_s: #z축 뒤 이동
                    real_game.player.dz -= real_game.player.speed

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    real_game.player.dx += real_game.player.speed
                
                if event.key == pygame.K_d:
                    real_game.player.dx -= real_game.player.speed
    
                if event.key == pygame.K_w:#z축 앞 이동
                    real_game.player.dz -= real_game.player.speed
                    
                if event.key == pygame.K_s: #z축 뒤 이동
                    real_game.player.dz += real_game.player.speed

            # 대화가 끝나면 대화 활성화 상태 해제
            if first_talk == 1:
                if current_dialogue_index >= len(talking["dialogues"]):
                    real_game.prevent2 = False
                    first_talk += 1
                    current_dialogue_index = 0  # 리셋
                    is_talking = False
                    first_talk = 2  # 대화 종료
            elif second_talk == 1:
                if current_dialogue_index >= len(talking["second"]):
                    real_game.prevent2 = False
                    second_talk += 1
                    current_dialogue_index = 0  # 리셋
                    is_talking = False
                    second_talk = 2  # 대화 종료


def check_player_position():
    import real_game
    global is_talking, first_talk, second_talk
    if -500 < real_game.player.x < 500 and -500 < real_game.player.z < 500 and first_talk != 2:
    # if True:
        is_talking = True
        if first_talk == 0:
            first_talk += 1
    elif -550 < real_game.player.x < -450 and -550 < real_game.player.z < -450 and second_talk != 2:
        is_talking = True
        if second_talk == 0:
            second_talk += 1
    else:
        is_talking = False  # 대화 종료

def draw_dialogue():
    import real_game
    if is_talking:
        dialogue_box_rect = pygame.Rect(50, real_game.screen_height - 150, real_game.screen_width - 100, 100)
        pygame.draw.rect(real_game.screen, DIALOGUE_BOX_COLOR, dialogue_box_rect)

        # Render dialogue text
        if first_talk == 1:
            if current_dialogue_index < len(talking["dialogues"]):
                text_surface = font.render(talking["dialogues"][current_dialogue_index], True, WHITE)
                text_rect = text_surface.get_rect(center=dialogue_box_rect.center)
                real_game.screen.blit(text_surface, text_rect)
        elif second_talk == 1:
            if current_dialogue_index < len(talking["second"]):
                text_surface = font.render(talking["second"][current_dialogue_index], True, WHITE)
                text_rect = text_surface.get_rect(center=dialogue_box_rect.center)
                real_game.screen.blit(text_surface, text_rect)
