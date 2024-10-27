import pygame
import math
import projection_3D
from settings import *
import piece
import map_loading
from player import *
import time
import animation
import bisect

#플레이어 세팅

aquire_piece_count = 0
texture_num = 0


#색칠 변수
color = 0

#키 누름 카운트
z_key_count =0

#블록 설치
blocks = []


def jumping():
    player.dy = -1.5  # 초기 속도로 시작


def setblock(texture_num):    
    nearestx_100 = round(player.x / 100) * 100
    nearesty_100 = round(player.y / 100) * 100 + 100
    nearestz_100 = round(player.z / 100) * 100
  
    map_loading.map_test.BLOCKS.append(map_loading.Block((nearestx_100,nearesty_100,nearestz_100),texture_num))

def blockremove():
    nearestx_100 = round(player.x / 100) * 100
    nearesty_100 = round(player.y / 100) * 100 + 100
    nearestz_100 = round(player.z / 100) * 100
        
    block_to_remove = (nearestx_100, nearesty_100, nearestz_100)
    
    for block in map_loading.map_test.BLOCKS:
        if block.pos == block_to_remove:
            map_loading.map_test.BLOCKS.remove(block)
            break
    
def aquire_piece():
    global aquire_piece_count
    
    if abs(player.x) - abs(piece.pieceblock.x) < 50 and abs(player.x) - abs(piece.pieceblock.x) > -50:
        if abs(player.y) - abs(piece.pieceblock.y) < 50 and abs(player.y) - abs(piece.pieceblock.y) > -50:
            if abs(player.z) - abs(piece.pieceblock.y) < 50 and abs(player.y) - abs(piece.pieceblock.y) > -50:
                aquire_piece_count += 1
            
# def warp():
#     for block in map_loading.map_test.BLOCKS:
#         player_x - block.x

# def check_wall_collision():
#     global player_x_d, player_y_VELOCITY, z_key_count, Front_collision, jump_count, time_elapsed, acceleration, initial_velocity, is_falling, player_y, player_x, player_z
#     # if player_moving == True:
#     if z_key_count == 0:
#         for block in map_loading.map_test.BLOCKS:
#             if player_x == block.x:
#                 pass
#                 #x좌표 기준으로 본인 발 밑에 있는 블록 감지
#             if block.y < 500:
#                 if block.x - player_x == 100:
#                     if player_x_d > 0:
#                         if is_3D == False:
#                             Front_collision = True
#                         else:
#                             if abs(block.z) - abs(player_z)  < 100 and abs(block.z) - abs(player_z) > -100:
#                                 Front_collision = True
                        

                        
#             # 플레이어의 밑면과 블록 윗면이 맞닿는 경우 (점프 상태에 따라 조건 변경)
#             if jump_count == 2:
#                 if 310 <= block.y - player_y <= 340 and - block.size - 50 < block.x - player_x < block.size + 50 and - block.size - 50 < block.z - player_z < block.size + 50:
#                     print("나중, 충돌된 거 : ",block.y)
#                     player_y_VELOCITY = 0
#                     time_elapsed = 0
#                     acceleration = 0
#                     initial_velocity = 0
#                     player_y = block.y - 325
#                     jump_count = 0
#                     is_falling = False
#                     break  # 충돌이 감지되면 루프 종료
#             else:
#                 if block.y - player_y == 325 and - block.size - 50 < block.x - player_x < block.size + 50 and -block.size - 50 < block.z - player_z < block.size + 50 and jump_count != 1:
#                     print("처음")
#                     time_elapsed = 0
#                     player_y_VELOCITY = 0
#                     initial_velocity = 0
#                     acceleration = 0
#                     jump_count = 0
#                     is_falling = False
#                     break  # 충돌이 감지되면 루프 종료
#         # 모든 블록을 검사한 후에도 충돌이 없으면 떨어짐 처리
#         if is_falling:
#             player_y_go()


def check_collision():
    xyz = [player.x,player.y,player.z]
    dxyz = [player.dx,player.dy,player.dz]
    result = []
    
    for block in map_loading.BLOCKS:
        block_xyz = (block.x,block.y,block.z)
        for i in [0,2]:
            if (abs(block_xyz[i] - (xyz[i] + dxyz[i]))<100) and (abs(block_xyz[(i+1)%3] - (xyz[(i+1)%3]))<100) and (abs(block_xyz[(i+2)%3] - (xyz[(i+2)%3]))<100):
                result.append(i)
                # print (block_xyz)
                # print (i)
                # print(xyz,dxyz)
        if (100<(player.y + player.dy)-block.y < 200) and (abs(block_xyz[2] - (xyz[2]))<100) and (abs(block_xyz[0] - (xyz[0]))<100):
            result.append(3)
        result.append(1)

    result2 = [0,0,0,0]
    for i in range(4):
        if i not in result:
            result2[i] = True
        else:
            result2[i] = False
    # print(result2)
    return result2
    

#플레이어 움직임 실시간 적용
def player_during():
    x_OK,y_OK,z_OK,head = check_collision()
    if x_OK:
        player.x += player.dx
    if y_OK:
        player.dy += GRAVITY
        player.y += player.dy
        player.jump_OK = False
    else:
        player.dy = 0
        if not head:
            player.jump_OK = True
    if z_OK and is_3D:
        player.z += player.dz
    elif z_OK and not is_3D:
        player.z = 100
    
    player.fake_z += 0.2 * (player.z - player.fake_z)
    player.fake_x += 0.2 * (player.x - player.fake_x)

    # print (player.x,player.y,player.z,player.dx,player.dy,player.dz)
    player.points = [
        [player.fake_x - player.size, player.y - 3*player.size], [player.fake_x + player.size, player.y - 3*player.size],
        [player.fake_x + player.size, player.y + player.size], [player.fake_x - player.size, player.y + player.size],
    ]

    player.range = (player.x-camera_pos[0])**2 + (player.y-50-camera_pos[1])**2 + (player.z-camera_pos[2])**2

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


def draw_square(square,color_set):
    temp_square = []
    for point in square[0:4]:
        temp_square.append(projection_3D.project_3d_or_2d((point[0],point[1],point[3]), camera_pos, angle_x, angle_y))
    square = temp_square
    if (None not in square):
        if (not are_all_points_collinear(square)):
            # 좌표가 한 직선 위에 있지 않으면 그리기
            pygame.draw.polygon(screen, color_set[0], square, 0)  # 내부를 채운 다각형
            pygame.draw.polygon(screen, color_set[1], square, 4)  # 테두리 두께 4

def cal_square(square,where):
    if (((where == 'front') and (square not in showing.squares_front)) or (square not in showing.squares)):#중복되는 것이 없는지 확인
        if (where == 'front'):#2D 계산할 때 쓰일 square은 따로 거리를 계산하지 않고 저장
            showing.squares_front.append(square)

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
def check_cube(points,texture):
    squares = [
    # 앞면
        [points[0], points[1], points[2], points[3], [texture[1],texture[3]]],

        # 뒷면
        [points[4], points[5], points[6], points[7], [texture[1],texture[3]]],

        # 왼쪽면
        [points[0], points[3], points[7], points[4], [texture[1],texture[3]]],

        # 오른쪽면
        [points[1], points[2], points[6], points[5], [texture[1],texture[3]]],

        # 윗면
        [points[0], points[1], points[5], points[4], [texture[0],texture[3]]],

        # 아랫면
        [points[3], points[2], points[6], points[7], [texture[2],texture[3]]]
    ]
    cal_square(squares[0],'front')
    for square in squares[1:6]:
        cal_square(square,'rest')


# 메인 루프
def mouse_rotate_check():
    global angle_x, angle_y
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # 각도 업데이트 (마우스 이동에 따라)

    angle_x += mouse_dx * mouse_sensitivity
    if (-math.pi/2<angle_y + mouse_dy * mouse_sensitivity<math.pi/2):
        angle_y += mouse_dy * mouse_sensitivity

def event_check():
    global condition, is_3D, target_camera_pos, color, z_key_count, texture_num
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if pygame.K_0 <= event.key <= pygame.K_9:
                texture_num = event.key - pygame.K_0

            if event.key == pygame.K_ESCAPE:
                condition =  "quit"
            if event.key == pygame.K_r:
                # 시점 전환 목표 설정
                is_3D = not is_3D

            if event.key == pygame.K_a:
                player.dx -= 25
            
            if event.key == pygame.K_d:
                player.dx += 25

            if event.key == pygame.K_w:#z축 앞 이동
                player.dz += 25
                
            if event.key == pygame.K_s: #z축 뒤 이동
                player.dz -= 25
            

            if event.key == pygame.K_z: #개발자 모드 실행
                if z_key_count == 0:
                    z_key_count = 1
                    color = 255                    
                else:
                    z_key_count = 0
                    color = 0
            if event.key == pygame.K_p: # 맵 세이브
                if z_key_count == 1:
                    map_loading.map_save()
            if event.key == pygame.K_l: # 맵 로딩
                if z_key_count == 1:
                    map_loading.map_load()
            if event.key == pygame.K_SPACE: 
                if z_key_count != 1:
                    if player.jump_OK:
                        jumping()
                    

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a: 
                if z_key_count == 0:
                    player.dx += 25
                else:
                    player.x -= 100
                    camera_pos[0] -= 100
            if event.key == pygame.K_w:
                if z_key_count == 0:
                    player.dz -= 25
                else:
                    player.z += 100
                    camera_pos[2] += 100
                    

                pass
            if event.key == pygame.K_d: 
                if z_key_count == 0:
                    player.dx -= 25
                else:
                    player.x += 100
                    camera_pos[0] += 100
            if event.key == pygame.K_s: 
                # player_stop()
                if z_key_count == 0:
                    player.dz += 25
                else:
                    player.z -= 100
                    camera_pos[2] -= 100

            if event.key == pygame.K_SPACE: 
                # player_stop()
                if z_key_count == 1:
                    player.y -= 100
                    camera_pos[1] -= 100

            if event.key == pygame.K_LSHIFT: 
                if z_key_count == 1:
                    player.y += 100
                    camera_pos[1] += 100


        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 휠 클릭을 감지
            if event.button == 3: # 개발자 블록 설치
                if z_key_count == 1:    
                    setblock(texture_num)
            elif event.button == 4:  # 휠을 위로 스크롤
                camera_pos[2] += camera_speed * 2  # 카메라를 앞으로 이동
            elif event.button == 5:  # 휠을 아래로 스크롤
                camera_pos[2] -= camera_speed * 2  # 카메라를 뒤로 이동
            elif event.button == 1:
                if z_key_count == 1:    
                    blockremove()

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

# def draw_player():
#     temp = []
#     for point in player.points:
#         temp.append(projection_3D.project_3d_or_2d((point[0],point[1],player.fake_z), camera_pos,angle_x,angle_y))
#     if None not in temp:
#         animation.draw_quad("player",temp)

def draw_screen():
    global blocks
    screen.fill((255, 255, 255))
    showing.squares = []
    showing.squares_front = []
    for block in map_loading.map_test.BLOCKS:
        block_3D_transition(block.points)
        check_cube(block.points,block.texture)
    showing.squares = sorted(showing.squares, key=lambda square: -square[5])
    square_5ths = [squares[5] for squares in showing.squares]

    # 내림차순 리스트를 오름차순으로 변환하여 bisect 사용
    reversed_values = square_5ths[::-1]
    position = bisect.bisect_left(reversed_values, player.range)

    # 내림차순이므로 위치를 반전하여 실제 위치 계산
    actual_position = len(showing.squares) - position
    # 블록 그리기
    # for block in map.BLOCKS:
    #     draw_cube(projection_3D.project_3d_or_2d(block.points, camera_pos, is_3D, angle_x, angle_y))

    # # 플레이어 그리기
    # draw_cube(projection_3D.project_3d_or_2d(playerblock.points, camera_pos, is_3D, angle_x, angle_y))

    # # pieceblock 그리기 (카메라 앵글 반영)
    # piece.pieceblock.update_points(camera_pos, angle_x, angle_y)
    # draw_real_piece(piece.pieceblock.projected_points)

    # pygame.display.flip()
    # clock.tick(60)
    if (is_3D):
        for i in range(actual_position):
            if actual_position != 0:
                draw_square(showing.squares[i][0:4],showing.squares[i][4])
        animation.anime()
        for i in range(actual_position,len(showing.squares)):
            # if actual_position != len(showing.squares):
            draw_square(showing.squares[i][0:4],showing.squares[i][4])
    else:
        for square in showing.squares_front:
            draw_square(square[0:4],square[4])
        animation.anime()
    if aquire_piece_count == 0:
        draw_real_piece(piece.pieceblock)
    pygame.display.flip()
    clock.tick(60)


def run():
    global condition, jump_count, acceleration
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    player_during()  # 플레이어 위치 업데이트 먼저
    camera_move()
    
    draw_screen()
    
    return condition