import pygame
import time
from settings import *

font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 36)  
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


dialogues = [
    "그렇게 그들의 차원은 평화를 되찾았다… 아마도…",
    "꼼짝없이 죽을 줄 알았지만 다행히 나도 내 차원으로 돌아올 수 있었고..",
    "뭐, 나름 잘 살고 있다.",
    "그래봐야 선과 점밖에 없는 무미건조한 세상이지만…",
    "...",
    "어쩌면 아주 긴 꿈을 꿨던 것이 아닐까..",
    "...",
    "“하긴 내가 세상을 구했다니..말도 안 되지…”",
    "...",
    "“그래. 놔줄 때도 됐다..”",
    "...",
    "“이 헤드셋.. 어차피 소리도 안 나오는데, 그냥 버릴까…”",
    "...", "...", "...",
    "어...?",
    "ㅏ...", "ㅏㅏㅏ..", "들리니?"
]

credits = [
    "BEYOND THE DIMENSION",
    "",
    "Team Dimension Breakers",
    "개발 : 이정웅, 장현우, 송강을",
    "애니메이션 : 최윤찬",
    "베타테스터 : 이재찬, 이준수",
    "카메라 감독 : 임하균"
    "",
    "폰트 : 배달의 민족 한나체, 배달의 민족 을지로체",
    "",
    "Main Theme : 📢BGM",
    "",
    "✔Track - 게임 시작!",
    "✔Music by 부금",
    "✔Watch : https://youtu.be/0aLKEeltie8"
]

def event_check():
    global condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition = "quit"
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition = "quit"
                return True
    return False

def run():
    global condition
    condition = "ending"
    fade_duration = 1.5
    fade_delay = 0.2
    blue_fade_start = 12

    screen.fill(white)
    pygame.display.update()

    for i, text in enumerate(dialogues):
        if event_check():
            return condition

        fade_color = blue if i >= blue_fade_start else black

        for alpha in range(0, 256, 5):
            if event_check():  # ESC키가 눌리면 즉시 종료
                return condition
            screen.fill(white)
            render_text = font.render(text, True, fade_color)
            render_text.set_alpha(alpha)
            text_rect = render_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(render_text, text_rect)
            pygame.display.update()
            pygame.time.delay(int(fade_duration * 1000 / 51))

        pygame.time.delay(int(fade_delay * 1000))

    pygame.display.update()
    screen.fill(black)
    pygame.time.delay(1000)

    y_offset = screen.get_height()
    while y_offset > -len(credits) * 50:
        if event_check():
            return condition

        screen.fill(black)
        for i, credit_text in enumerate(credits):
            render_text = font.render(credit_text, True, white)
            text_rect = render_text.get_rect(center=(screen.get_width() // 2, y_offset + i * 50))
            screen.blit(render_text, text_rect)

        pygame.display.update()
        pygame.time.delay(20)
        y_offset -= 1

    condition = "start_menu"
    return condition
