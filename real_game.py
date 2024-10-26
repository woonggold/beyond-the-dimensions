import pygame
import math
import projection_3D
from settings import *
import Player
import json
import piece
import map_loading
# 파이게임 초기화


#플레이어 세팅
player_x = Player.playerblock.x
player_y = Player.playerblock.y
player_z = Player.playerblock.z
player_mass = 1
Moving_left = False
x_back = False
x_go = False
Y_down = False
Y_up = False
aquire_piece_count = 0

#캐릭터 충동 처리


#플레이어 속도 변화랑
player_x_d = 0
player_y_VELOCITY = 0
player_z_d = 0
jump_count = 1
acceleration = 0
#개발자모드 y이동 속도
player_y_d = 0

#플레이어 움직임 함수

#색칠 변수
color = 0

#키 누름 카운트
z_key_count =0

#블록 설치
blocks = []

#블록 list


# def player_jump():
#     global jump_count, player_y
#     if jump_count == 1:
#         jump_count = 0
#         if player_y_VELOCITY > 0:
#                 F = (0.5 * player_mass * (player_y_VELOCITY * player_y_VELOCITY))
#         else:
#             F = -(0.5 * player_mass * (player_y_VELOCITY * player_y_VELOCITY))
        
#         player_y = 1/2 * player_mass * player_y_d^2


def gravity():
    global condition, player_x, player_y, player_z, acceleration, z_key_count
    
    if z_key_count == 0:
        min_x, min_y, min_z = player_x - 50, player_y + 100, player_z - 50
        max_x, max_y, max_z = player_x + 50, player_y + 100, player_z + 50

        is_within_bounds = False  # 초기화하여 범위를 벗어났는지 확인

        for block in map_loading.map_test.BLOCKS:
            block_min_x = block.x - block.size
            block_max_x = block.x + block.size
            block_min_y = block.y - block.size
            block_max_y = block.y
            block_min_z = block.z - block.size
            block_max_z = block.z + block.size

            # 플레이어의 범위가 블록 범위와 겹치는지 확인
            if (min_x <= block_max_x and max_x >= block_min_x) and \
            (min_y <= block_max_y and max_y >= block_min_y) and \
            (min_z <= block_max_z and max_z >= block_min_z):
                print("안 벗어남")
                acceleration = 0  # 겹치는 경우 가속도 0으로 설정
                is_within_bounds = True  # 범위 내에 있음을 표시
                break  # 하나라도 겹치면 더 이상 확인할 필요 없음

        if not is_within_bounds:
            go_to_main()
            return True
        return False

# 범위를 벗어났을 때 실행할 함수
def go_to_main():
    print("범위를 벗어남")

def map_save():
    blocks_dict_x = []
    blocks_dict_y = []
    blocks_dict_z = []
    for block in map_loading.map_test.BLOCKS:
        blocks_dict_x.append(block.x)
        blocks_dict_y.append(block.y)
        blocks_dict_z.append(block.z)
    
    separated_data = {
        "x": blocks_dict_x,
        "y": blocks_dict_y,
        "z": blocks_dict_z,  
    }
    
    final_data = {
        "Blocks": separated_data, 
    }
    mapname = input("저장할 맵 이름을 입력해 주세요: ")

    with open(mapname+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(final_data, json_file, ensure_ascii=False, indent=4)    
    print("저장됨")
        
def map_load():
    mapname = input("불러올 맵 이름을 입력해 주세요: ")
    with open(mapname+'.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)    
    for i in range(len(data["Blocks"]["x"])):
        map_loading.BLOCKS.append(map_loading.Block((data["Blocks"]["x"][i],data["Blocks"]["y"][i],data["Blocks"]["z"][i])))

    print("로드됨")
   
def go_to_main():
    player_y_go()

def player_stop():
    global player_x_d, player_y_VELOCITY, player_z_d, jump_count, player_moving, Moving_left, player_y_d, x_back, x_go, Y_down, Y_up
    player_x_d = 0
    player_y_VELOCITY = 0
    player_z_d = 0
    jump_count = 1
    player_moving = False
    Moving_left = False
    player_y_d = 0
    x_back = False
    x_go = False
    Y_down = False
    Y_up = False

def player_right_go():
    global player_x_d, x_go
    player_x_d = 25
    x_go = True
    

def player_left_go():
    global player_x_d, Moving_left, x_back
    player_x_d = -25
    Moving_left = True
    x_back = True

def player_z_go():
    global player_z_d
    player_z_d = 25

    
def player_back_z_go():
    global player_z_d
    player_z_d = -25


def player_y_go():
    global player_y_VELOCITY, acceleration
    acceleration += 0.05
    player_y_VELOCITY = 0.01 + acceleration
    

def develop_y_go_back():
    global player_y_d, Y_down
    player_y_d += -25
    Y_down = True

def develop_y_go():
    global player_y_d, Y_up
    player_y_d += 25
    Y_up = True

def setblock():    
    nearestx_100 = round(player_x / 100) * 100
    nearestz_100 = round(player_z / 100) * 100
    
    # -100  -4
    # -75   -3
    # -50-- -2
    # -25 -- -1 -- 100
    # 0 -- 0 -- 100
    # 25 -- 1 -- 200
    # 50 -- 2 -- 200
    # 75 --- 3 --300
    # 100 -- 4 -- 400
    # 125 -- 5 -- 400
    # 150 -- 6 --500  --3
    # 175 --- 7 -- 500 -- 3
    # 발밑 
    # 500
    if player_y > 0:
        player_cal = player_y / 25
        player_cal_m = player_cal // 2
        nearesty_100 = player_cal_m * 100 + 200
    else:
        player_cal = abs(player_y) / 25
        player_cal_m = ((player_cal) // 2) 
        nearesty_100 = 100 - (player_cal_m * 100)

    
  
    map_loading.BLOCKS.append(map_loading.Block((nearestx_100,nearesty_100,nearestz_100)))
    
    # print('블럭설치')
    
def aquire_piece():
    global aquire_piece_count, piece_img
    
    if abs(player_x) - abs(piece.pieceblock.x) < 50 and abs(player_x) - abs(piece.pieceblock.x) > -50:
        if abs(player_y) - abs(piece.pieceblock.y) < 50 and abs(player_y) - abs(piece.pieceblock.y) > -50:
            aquire_piece_count += 1
            
def next_stage():
    pass


def check_wall_collision():
    global player_moving, player_x_d, Moving_left, player_y_VELOCITY, z_key_count
    # if player_moving == True:
    if z_key_count == 0:
        for block in map_loading.map_test.BLOCKS:
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
            if block.y - player_y == 325 and block.x - player_x < 100 and block.x - player_x > -100 and block.z - player_z < 100 and block.z - player_z > -100:
                player_y_VELOCITY = 0
            

#플레이어 움직임 실시간 적용
def player_during():
    global player_x, player_y, player_z, player_moving, z_key_count, Y_down, Y_up, x_go, x_back
    check_wall_collision()
    aquire_piece()
    player_moving = True
    player_x += player_x_d
    player_y += player_y_d
    if z_key_count == 0:
        player_y += player_y_VELOCITY
    player_z += player_z_d
    
    
    if z_key_count == 1:

        if Y_down == True:
            camera_pos[1] -= camera_speed
        if Y_up == True:
            camera_pos[1] += camera_speed
        if x_go == True:
            camera_pos[0] += camera_speed
        if x_back == True:
            camera_pos[0] -= camera_speed
    
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



# def draw_line(one,two):
#     global color
    
#     if all((one,two)):
#         pygame.draw.aaline(screen, (color, 0, 0), one, two, 1)

# def draw_line_piece(one,two):
#     global color
    
#     if all((one,two)):
#         pygame.draw.aaline(screen, (255, 0, 0), one, two, 1)
        
# def draw_piece(piece):
#     for i in range(len(piece)):
#         x1, y1 = piece[i]
#         x2, y2 = piece[(i + 1) % len(piece)]  

#         draw_line_piece((x1, y1), (x2, y2))
    
# # def draw_real_piece(points):
# #     piece = [points[0], points[1], points[2], points[3]]

# #     draw_square(piece)
def draw_real_piece(piece_block):
    global piece_img,aquire_piece_count
    x, y, z = piece_block.x, piece_block.y, piece_block.z,
    dx = abs(x-camera_pos[0])
    dy = abs(y-camera_pos[1])
    dz = abs(z-camera_pos[2])
    piece_range = (dx**2+dy**2+dz**2)**(1/2)
    result = projection_3D.project_3d_or_2d((x,y,z), camera_pos,angle_x,angle_y)

    piece_img = pygame.image.load(f"{script_dir}//images//차원조각.png").convert_alpha()
    piece_rect = piece_img.get_rect()
    piece_width, piece_height = piece_rect.width, piece_rect.height 
    modified_img = pygame.transform.scale(piece_img, (200*piece_width / piece_range, 200*piece_height / piece_range))
    modified_rect = modified_img.get_rect()
    modified_width, modified_height = modified_rect.width, modified_rect.height 
    if result != None:
        screen.blit(modified_img, (result[0] - (modified_width / 2), result[1] - (modified_height / 2)))
    
    
# 큐브의 면을 그리는 함수

def is_collinear(p1, p2, p3):
    # 기울기: (y2 - y1) / (x2 - x1) = (y3 - y1) / (x3 - x1)
    # 두 직선의 기울기가 같으면 한 직선 위에 있다.
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) == (p2[1] - p1[1]) * (p3[0] - p1[0])

def are_all_points_collinear(points):
    # 4개의 점 중 첫 번째 점과 나머지 세 점의 기울기가 모두 같으면 한 직선 위에 있음
    p1, p2, p3, p4 = points
    return is_collinear(p1, p2, p3) or is_collinear(p1, p2, p4) or is_collinear(p1, p3, p4) or is_collinear(p3, p2, p4)


def draw_square(square):
    temp_square = []
    for point in square[0:4]:
        temp_square.append(projection_3D.project_3d_or_2d((point[0],point[1],point[3]), camera_pos, angle_x, angle_y))
    square = temp_square
    if (None not in square):
        if (not are_all_points_collinear(square)):
            # 좌표가 한 직선 위에 있지 않으면 그리기
            pygame.draw.polygon(screen, (255,255,255), square, 0)  # 내부를 채운 다각형
            pygame.draw.polygon(screen, (color,0,0), square, 4)  # 테두리 두께 4

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
    global condition, is_3D, target_camera_pos, color, z_key_count, player_y_VELOCITY, acceleration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition =  "quit"
            if event.key == pygame.K_r:
                # 시점 전환 목표 설정
                is_3D = not is_3D
            if event.key == pygame.K_a:
                player_left_go()
                
            if event.key == pygame.K_d: 
                player_right_go()
                pass
            if event.key == pygame.K_w:#z축 앞 이동
                player_z_go()
            if event.key == pygame.K_s: #z축 뒤 이동
                player_back_z_go() 
            

            if event.key == pygame.K_z: #개발자 모드 실행
                if z_key_count == 0:
                    z_key_count = 1
                    color = 255
                    
                else:
                    z_key_count = 0
                    color = 0
            if event.key == pygame.K_p: # 맵 세이브
                if z_key_count == 1:
                    map_save()
            if event.key == pygame.K_l: # 맵 로딩
                if z_key_count == 1:
                    map_load()
            if event.key == pygame.K_LSHIFT:
                if z_key_count == 1:
                    develop_y_go()
            if event.key == pygame.K_SPACE: 
                if z_key_count == 1:
                    develop_y_go_back()
        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_a: 
                player_stop()
                pass
            if event.key == pygame.K_w:
                player_stop()
                pass
            if event.key == pygame.K_d: 
                player_stop()
            if event.key == pygame.K_s: 
                player_stop()
            if event.key == pygame.K_SPACE: 
                player_stop()
            if event.key == pygame.K_LSHIFT: 
                player_stop()


        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 휠 클릭을 감지
            if event.button == 3: # 개발자 블록 설치
                if z_key_count == 1:    
                    setblock()
            elif event.button == 4:  # 휠을 위로 스크롤
                camera_pos[2] += camera_speed * 2  # 카메라를 앞으로 이동
            elif event.button == 5:  # 휠을 아래로 스크롤
                camera_pos[2] -= camera_speed * 2  # 카메라를 뒤로 이동

def camera_move():
    # 부드럽게 이동
    global camera_pos, z_key_count
    
    if z_key_count == 0:
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
    global blocks
    screen.fill((255, 255, 255))
    showing.squares = []
    showing.squares_front = []
    for block in map_loading.map_test.BLOCKS:
        block_3D_transition(block.points)
        check_cube(block.points)
    check_cube(Player.playerblock.points)
    showing.squares = sorted(showing.squares, key=lambda square: -square[4])

    # 블록 그리기
    # for block in map.BLOCKS:
    #     draw_cube(projection_3D.project_3d_or_2d(block.points, camera_pos, is_3D, angle_x, angle_y))

    # # 플레이어 그리기
    # draw_cube(projection_3D.project_3d_or_2d(Player.playerblock.points, camera_pos, is_3D, angle_x, angle_y))

    # # pieceblock 그리기 (카메라 앵글 반영)
    # piece.pieceblock.update_points(camera_pos, angle_x, angle_y)
    # draw_real_piece(piece.pieceblock.projected_points)

    # pygame.display.flip()
    # clock.tick(60)

    if (is_3D):
        for square in showing.squares:
            draw_square(square[0:4])
    else:
        for square in showing.squares_front:
            draw_square(square[0:4])
    if aquire_piece_count == 0:
        draw_real_piece(piece.pieceblock)
    pygame.display.flip()
    clock.tick(60)


def run():
    global condition
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    player_during()  # 플레이어 위치 업데이트 먼저
    camera_move()
    draw_screen()
    gravity()
    
    return condition