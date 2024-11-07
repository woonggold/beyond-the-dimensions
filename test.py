import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("키보드로 조작 가능한 사각형")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 사각형 속성
rect_x, rect_y = WIDTH // 2, HEIGHT // 2
rect_size = 50
speed = 5

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 상태 확인
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect_x -= speed
    if keys[pygame.K_RIGHT]:
        rect_x += speed
    if keys[pygame.K_UP]:
        rect_y -= speed
    if keys[pygame.K_DOWN]:
        rect_y += speed

    # 화면 업데이트
    screen.fill(WHITE)  # 배경 색상
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_size, rect_size))  # 사각형 그리기
    pygame.display.flip()  # 화면에 그리기

    # 프레임 속도 조절
    pygame.time.Clock().tick(60)