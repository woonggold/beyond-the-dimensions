import pygame
import math
import projection_3D
from settings import *
import map_loading
# 파이게임 초기화



# 큐브의 8개 꼭짓점 좌표 생성 함수


# def draw_line(one,two):
#     if all((one,two)):
#         pygame.draw.aaline(screen, (0, 0, 0), one, two, 1)

def draw_square(square):
    temp_square = []
    for point in square[0:4]:
        temp_square.append(projection_3D.project_3d_or_2d(point, camera_pos, angle_x, angle_y))
    square = temp_square
    
    if (None not in square):
        out = 0
        delta = -10
        for pixel in square:
            if not (0-delta<pixel[0]<screen_width+delta and 0-delta<pixel[1]<screen_height+delta):
                out += 1
        if out == 4:
            return #함수종료
        if (abs(square[1][1]-square[2][1]) >= screen_height) or (abs(square[2][1]-square[3][1]) >= screen_height):
            return
        if (abs(square[1][0]-square[2][0]) >= screen_width) or (abs(square[2][1]-square[3][1]) >= screen_height):
            return
        pygame.draw.polygon(screen, (255,255,255), square, 0)  # 내부를 채운 다각형
        pygame.draw.polygon(screen, (0,0,0), square, 10)  # 테두리 두께 1
    # draw_line(square[0],square[1])
    # draw_line(square[1],square[2])
    # draw_line(square[2],square[3])
    # draw_line(square[3],square[0])

def cal_square(square,where):
    if (((where == 'front') and (square not in showing.squares_front)) or (square not in showing.squares)):#중복되는 것이 없는지 확인
        if (where == 'front'):#2D 계산할 때 쓰일 square은 따로 거리를 계산하지 않고 저장
            showing.squares_front.append(square)

        # x = (square[0][0] + square[1][0] + square[2][0] + square[3][0])/(cube_size/2-1)
        # y = (square[0][1] + square[1][1] + square[2][1] + square[3][1])/(cube_size/2-1)
        # z = (square[0][3] + square[1][3] + square[2][3] + square[3][3])/(cube_size/2-1)
        x = (square[0][0] + square[1][0] + square[2][0] + square[3][0])//4
        y = (square[0][1] + square[1][1] + square[2][1] + square[3][1])//4
        z = (square[0][3] + square[1][3] + square[2][3] + square[3][3])//4



        dx = x - camera_pos[0]
        dy = y - camera_pos[1]
        dz = z - camera_pos[2]
        range = dx**2 + dy**2 + dz**2

        square.append(range)

        showing.squares.append(square)

# 큐브의 면을 그리는 함수
def check_cube(points):
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
    cal_square(squares[0],'front')
    for square in squares[1:6]:
        cal_square(square,'rest')


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
            if event.key == pygame.K_r:
                # 시점 전환 목표 설정
                is_3D = not is_3D
                # if is_3D:
                #     # target_camera_pos[0] = 0  # 탑뷰 카메라 위치 설정
                #     target_camera_pos[1] -= 250
                #     target_camera_pos[2] -= 250 # 바닥이 보이도록 카메라 높이 조정
                # else:
                #     # target_camera_pos[0] = 0  # 플랫포머뷰 카메라 위치 설정
                #     target_camera_pos[1] += 250
                #     target_camera_pos[2] += 250
        

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:  # W 키 -> 앞으로 이동
        camera_pos[2] += camera_speed  # Z축 이동 (앞으로)
    if keys[pygame.K_s]:  # S 키 -> 뒤로 이동
        camera_pos[2] -= camera_speed  # Z축 이동 (뒤로)
    if keys[pygame.K_a]:  # A 키 -> 왼쪽으로 이동
        camera_pos[0] -= camera_speed  # X축 이동 (왼쪽)
    if keys[pygame.K_d]:  # D 키 -> 오른쪽으로 이동
        camera_pos[0] += camera_speed  # X축 이동 (오른쪽)
    if keys[pygame.K_SPACE]:  # Space 키 -> 위로 이동
        camera_pos[1] -= camera_speed  # Y축 이동 (위로)
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Shift 키 -> 아래로 이동
        camera_pos[1] += camera_speed  # Y축 이동 (아래로)
def camera_move():
    # 부드럽게 이동
    global camera_pos
    for i in range(3):
        camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1


def block_3D_transition(points):
    global camera_pos
    for point in points:
    # 부드럽게 이동
    
        if is_3D == False:
            
            x, y = point[0],point[1]
            if(abs(100 - point[3])>10):
                point[3] += (100 - point[3]) * 0.2
            else:
                point[3] = 100
            z = point[3]
    
        else:
            x, y = point[0],point[1]
            if(abs(point[2] - point[3])>10):
                point[3] += (point[2] - point[3]) * 0.2
            else:
                point[3] = point[2]
            z = point[3]

        point = x,y,point[2],z


def draw_screen():
    screen.fill((255, 255, 255))
    showing.squares = []
    showing.squares_front = []
    for block in map_loading.map_test:
        block_3D_transition(block.points)
        check_cube(block.points)
    showing.squares = sorted(showing.squares, key=lambda square: -square[4])

    if (is_3D):
        for square in showing.squares:
            draw_square(square[0:4])
    else:
        for square in showing.squares_front:
            draw_square(square[0:4])
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