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
player_x_d = 0
player_y_VELOCITY = 0
player_z_d = 0
jump_count = 1

#플레이어 움직임 함수

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
    jump_count = 1
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

def player_y_go():
    global player_y_VELOCITY
    player_y_VELOCITY = 5

# def check_wall():


def check_wall_collision():
    global player_moving, player_x_d, Moving_left
    # if player_moving == True:
    for block in map.BLOCKS:
        if player_x == block.x:
            pass
            #x좌표 기준으로 본인 발 밑에 있는 블록 감지
        if block.y < 500:
            if block.x - player_x == 100:
                if Moving_left == False:
                    if is_3D == False:
                        player_x_d = 0
                    else:
                        if abs(block.z) - abs(player_z)  < 100 and abs(block.z) - abs(player_z) > -100:
                            player_x_d = 0

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
            if event.key == pygame.K_LEFT: #뒤 이동
                player_left_go()
                
            if event.key == pygame.K_RIGHT: #앞이동
                player_right_go()
                pass
            if event.key == pygame.K_UP:#z축 앞 이동
                player_z_go()
            if event.key == pygame.K_DOWN: #z축 뒤 이동
                player_back_z_go() 

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
    screen.fill((255, 255, 255))

    for block in map.BLOCKS:
        draw_cube(projection_3D.project_3d_or_2d(block.points,camera_pos,is_3D,angle_x,angle_y))

    draw_cube(projection_3D.project_3d_or_2d(Player.playerblock.points,camera_pos,is_3D,angle_x,angle_y))
    

    pygame.display.flip()
    clock.tick(60)

def run():
    global condition
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    camera_move()
    draw_screen()
    player_during()  # 플레이어 위치 업데이트 먼저
    camera_move()
    draw_screen()
    
    return condition