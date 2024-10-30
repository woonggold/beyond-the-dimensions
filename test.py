
import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Polygon with Shadow Effect")

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SHADOW_COLOR = (50, 50, 50)

# 주 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 화면 지우기
    screen.fill(WHITE)

    # 그림자 효과: 테두리 그리기
    pygame.draw.rect(screen, SHADOW_COLOR, (0, 0, width, height), border_radius=40)  # 그림자


    # 마우스 위치 가져오기
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 다각형의 꼭짓점 설정 (정사각형)
    size = 50  # 정사각형 크기
    polygon_points = [
        (mouse_x - size // 2, mouse_y - size // 2),
        (mouse_x + size // 2, mouse_y - size // 2),
        (mouse_x + size // 2, mouse_y + size // 2),
        (mouse_x - size // 2, mouse_y + size // 2),
    ]

    # 다각형 그리기
    pygame.draw.polygon(screen, RED, polygon_points)

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()