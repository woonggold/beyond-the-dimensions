import pygame
import math
import projection_3D
from settings import *
import Player
# 파이게임 초기화


#플레이어 세팅
player_x = Player.playerblock.x
player_y = Player.playerblock.y
player_z = Player.playerblock.z
player_mass = 1
Moving_left = False

#캐릭터 충동 처리


#플레이어 속도 변화랑
initial_velocity = 0
player_x_d = 0
time_elapsed = 0
player_y_VELOCITY = 0
player_z_d = 0
jump_count = 0
acceleration = 0
#개발자모드 y이동 속도
player_z_y = 0

#플레이어 움직임 함수

#색칠 변수
color = 0

#키 누름 카운트
z_key_count =0

#블록 설치
blocks = []

# def player_jump():
#     global jump_count, player_y
#     if jump_count == 1:
#         jump_count = 0
#         if player_y_VELOCITY > 0:
#                 F = (0.5 * player_mass * (player_y_VELOCITY * player_y_VELOCITY))
#         else:
#             F = -(0.5 * player_mass * (player_y_VELOCITY * player_y_VELOCITY))
        
#         player_y = 1/2 * player_mass * player_y_d^2

def player_stop():
    global player_x_d, player_y_VELOCITY, player_z_d, jump_count, player_moving, Moving_left
    player_x_d = 0
    player_y_VELOCITY = 0
    player_z_d = 0
    player_moving = False
    Moving_left = False

def player_right_go():
    global player_x_d
    player_x_d = 25

def player_left_go():
    global player_x_d, Moving_left
    player_x_d = -25
    Moving_left = True

def player_z_go():
    global player_z_d
    player_z_d = 25
    
def player_back_z_go():
    global player_z_d
    player_z_d = -25

# 중력 가속도 상수 (m/s^2)
GRAVITY = 9.8  
time_elapsed = 0  # 시간 변수

def player_y_go():
    global player_y_VELOCITY, jump_count, time_elapsed, initial_velocity
    time_elapsed += 0.1 
    player_y_VELOCITY = initial_velocity + 9.8 * time_elapsed  # v = v0 + at

    if player_y_VELOCITY > 0:  
        jump_count = 2  

def jumping():
    global player_y_VELOCITY, initial_velocity, jump_count, time_elapsed
    jump_count = 1  
    time_elapsed = 0 
    initial_velocity = -15  
    player_y_VELOCITY = initial_velocity  # 초기 속도로 시작


def develop_y_go():
    global player_y_VELOCITY, acceleration, jump_count
    acceleration += 0.05
    player_y_VELOCITY = player_y_VELOCITY + acceleration

def setblock():
    nearestx_100 = round(player_x / 100) * 100
    nearestz_100 = round(player_z / 100) * 100
    map_loading.BLOCKS.append(map_loading.Block((nearestx_100,500,nearestz_100),50))
    
    # print('블럭설치')

def check_wall_collision():
    global player_moving, player_x_d, Moving_left, player_y_VELOCITY, is_falling, jump_count, player_y, time_elapsed, acceleration, initial_velocity
    is_falling = True  # 기본적으로 떨어지는 상태로 설정

    for block in map.BLOCKS:
        if player_x == block.x:
            pass 
        
        # x축에서 벽 충돌 감지
        if block.y < 500:
            if block.x - player_x == 100:
                if not Moving_left:
                    if not is_3D:
                        player_x_d = 0
                    elif abs(block.z - player_z) < 100:
                        player_x_d = 0 
        
        # 플레이어의 밑면과 블록 윗면이 맞닿는 경우 (점프 상태에 따라 조건 변경)
        if jump_count == 2:
            if 310 <= block.y - player_y <= 340 and - block.size - 50 < block.x - player_x < block.size + 50 and - block.size - 50 < block.z - player_z < block.size + 50:
                print("나중, 충돌된 거 : ",block.y)
                player_y_VELOCITY = 0
                time_elapsed = 0
                acceleration = 0
                initial_velocity = 0
                player_y = block.y - 325
                jump_count = 0
                is_falling = False
                break  # 충돌이 감지되면 루프 종료
        else:
            if block.y - player_y == 325 and - block.size - 50 < block.x - player_x < block.size + 50 and -block.size - 50 < block.z - player_z < block.size + 50 and jump_count != 1:
                print("처음")
                time_elapsed = 0
                player_y_VELOCITY = 0
                initial_velocity = 0
                acceleration = 0
                jump_count = 0
                is_falling = False
                break  # 충돌이 감지되면 루프 종료

    # 모든 블록을 검사한 후에도 충돌이 없으면 떨어짐 처리
    if is_falling:
        player_y_go()



            

#플레이어 움직임 실시간 적용
def player_during():
    global player_x, player_y, player_z, player_moving
    check_wall_collision()
    player_moving = True
    player_x += player_x_d
    player_y += player_y_VELOCITY
    player_z += player_z_d
    
    Player.playerblock.pos = (player_x, player_y, Player.playerblock.z)  
    Player.playerblock.x = player_x  
    Player.playerblock.y = player_y
    Player.playerblock.z = player_z

    if is_3D:
        Player.playerblock.points = [
        [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), Player.playerblock.z - Player.playerblock.size, Player.playerblock.z - Player.playerblock.size],
        [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), Player.playerblock.z - Player.playerblock.size, Player.playerblock.z - Player.playerblock.size],
        [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), Player.playerblock.z - Player.playerblock.size, Player.playerblock.z - Player.playerblock.size],
        [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), Player.playerblock.z - Player.playerblock.size, Player.playerblock.z - Player.playerblock.size],
        [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), Player.playerblock.z + Player.playerblock.size, Player.playerblock.z + Player.playerblock.size],
        [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), Player.playerblock.z + Player.playerblock.size, Player.playerblock.z + Player.playerblock.size],
        [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), Player.playerblock.z + Player.playerblock.size, Player.playerblock.z + Player.playerblock.size],
        [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), Player.playerblock.z + Player.playerblock.size, Player.playerblock.z + Player.playerblock.size]
    ]

    else:
        
        Player.playerblock.points = [
            [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), 100, 100],
            [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), 100, 100],
            [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), 100, 100],
            [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), 100, 100],
            [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), 100, 100],
            [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y - Player.playerblock.size), 100, 100],
            [Player.playerblock.x + Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), 100, 100],
            [Player.playerblock.x - Player.playerblock.size, 2 * (Player.playerblock.y + Player.playerblock.size), 100, 100]
        ]
        
        


    

# 큐브의 8개 꼭짓점 좌표 생성 함수



def draw_line(one,two):
    global color
    
    if all((one,two)):
        pygame.draw.aaline(screen, (color, 0, 0), one, two, 1)

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
        [points[0], points  [1], points[5], points[4]],

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
    global condition, is_3D, target_camera_pos, color, z_key_count, jump_count
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition =  "quit"
            if event.key == pygame.K_SPACE:
                # 시점 전환 목표 설정
                is_3D = not is_3D
            if event.key == pygame.K_e:
                if jump_count == 0:
                    jumping()
            if event.key == pygame.K_LEFT: #뒤 이동
                player_left_go()
                
            if event.key == pygame.K_RIGHT: #앞이동
                player_right_go()
                pass
            if event.key == pygame.K_UP:#z축 앞 이동
                player_z_go()
            if event.key == pygame.K_DOWN: #z축 뒤 이동
                player_back_z_go() 
            
            if event.key == pygame.K_w: # 개발자 블록 설치
                if z_key_count == 1:
                    setblock()
            if event.key == pygame.K_z: #개발자 모드 실행
                if z_key_count == 0:
                    z_key_count = 1
                    color = 255
                else:
                    z_key_count = 0
                    color = 0
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT: 
                player_stop()
                pass
            if event.key == pygame.K_RIGHT:
                player_stop()
                pass
            if event.key == pygame.K_UP: 
                player_stop()
            if event.key == pygame.K_DOWN: 
                player_stop()


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
    global blocks
    screen.fill((255, 255, 255))

    for block in map.BLOCKS:
        draw_cube(projection_3D.project_3d_or_2d(block.points,camera_pos,is_3D,angle_x,angle_y))

    draw_cube(projection_3D.project_3d_or_2d(Player.playerblock.points,camera_pos,is_3D,angle_x,angle_y))
    

    pygame.display.flip()
    clock.tick(60)

def run():
    global condition, jump_count, acceleration
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    camera_move()
    draw_screen()
    player_during()  # 플레이어 위치 업데이트 먼저
    camera_move()
    draw_screen()
    print(jump_count)
    
    return condition