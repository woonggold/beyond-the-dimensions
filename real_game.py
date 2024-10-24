import pygame
import math
import projection_3D
from settings import *
# 파이게임 초기화


# 큐브의 8개 꼭짓점 좌표 생성 함수


def draw_line(one,two):
    if all((one,two)):
        pygame.draw.aaline(screen, (0, 0, 0), one, two, 1)

def draw_square(square):
    checked = True
    
    if (checked):
        draw_line(square[0],square[1])
        draw_line(square[1],square[2])
        draw_line(square[2],square[3])
        draw_line(square[3],square[0])
# 큐브의 면을 그리는 함수
def draw_cube(points):
    squares = [
    # 앞면
        [points[0], points[1], points[2], points[3]],

        # 뒷면
        [points[4], points[5], points[6], points[7]],

        # 왼쪽면
        [points[0], points[3], points[7], points[4]],

        # 오른쪽면
        [points[1], points[2], points[6], points[5]],

        # 윗면
        [points[0], points[1], points[5], points[4]],

        # 아랫면
        [points[3], points[2], points[6], points[7]]
    ]
    for square in squares:
        draw_square(square)

    if is_3D:
        # 뒷면
        draw_line(points[4], points[5])
        draw_line(points[5], points[6])
        draw_line(points[6], points[7])
        draw_line(points[7], points[4])

        # 앞면과 뒷면을 연결하는 선들
        draw_line(points[0], points[4])
        draw_line(points[1], points[5])
        draw_line(points[2], points[6])
        draw_line(points[3], points[7])

# 바닥 그리기 함수
# def draw_floor(camera_pos):
#     floor_projected = [project_3d_to_2d(point, camera_pos) for point in floor_points]
    
#     if None not in floor_projected:
#         pygame.draw.polygon(screen, (100, 100, 100), floor_projected)  # 바닥을 그린다

# 메인 루프
def mouse_rotate_check():
    global angle_x, angle_y
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # 각도 업데이트 (마우스 이동에 따라)

    angle_x += mouse_dx * mouse_sensitivity
    if (-math.pi/2<angle_y + mouse_dy * mouse_sensitivity<math.pi/2):
        angle_y += mouse_dy * mouse_sensitivity

def event_check():
    global condition, is_3D, target_camera_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition =  "quit"
            if event.key == pygame.K_SPACE:
                # 시점 전환 목표 설정
                is_3D = not is_3D
        

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 휠 클릭을 감지
            if event.button == 4:  # 휠을 위로 스크롤
                target_camera_pos[2] += camera_speed * 2  # 카메라를 앞으로 이동
            elif event.button == 5:  # 휠을 아래로 스크롤
                target_camera_pos[2] -= camera_speed * 2  # 카메라를 뒤로 이동

def camera_move():
    # 부드럽게 이동
    global camera_pos
    for i in range(3):
        camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1

def draw_screen():
    screen.fill((255, 255, 255))

    for block in map.BLOCKS:
        draw_cube(projection_3D.project_3d_or_2d(block.points,camera_pos,is_3D,angle_x,angle_y))
    pygame.display.flip()
    clock.tick(60)

def run():
    global condition
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    camera_move()
    draw_screen()
    return condition