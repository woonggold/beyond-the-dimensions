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



def setblock(texture_num):    
    nearestx_100 = round(player.x / 100) * 100
    nearesty_100 = round(player.y / 100) * 100 + 100
    nearestz_100 = round(player.z / 100) * 100
    if texture_num == 9:
        warpname = input("워프 이름을 작성해 주세요: ")
        warp_name_list.append(warpname)
        warp_block_x_list.append(nearestx_100)
        warp_block_y_list.append(nearesty_100)
        warp_block_z_list.append(nearestz_100)
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
            

def check_overlap(block_min, block_max, player_min, player_max):
    return block_min < player_max and block_max > player_min

def check_collision():

    #check_collision[n][0] 은 +쪽, [n][1]은 -쪽
    xyz = [player.x,player.y,player.z]
    dxyz = [player.dx * delta_time,player.dy * delta_time,player.dz * delta_time]
    result = []
    k = [[0,0],[0,0],[0,0]]
    
    for block in map_loading.BLOCKS:
        bxyz = (block.x, block.y, block.z)

        for i in range(3):
            # 플레이어의 현재 위치에서 경계 값을 더한 값
            play_plus = (xyz[i] + player.border[i][0], xyz[(i + 1) % 3] + player.border[(i + 1) % 3][0], xyz[(i + 2) % 3] + player.border[(i + 2) % 3][0])
            play_minus = (xyz[i] + player.border[i][1], xyz[(i + 1) % 3] + player.border[(i + 1) % 3][1], xyz[(i + 2) % 3] + player.border[(i + 2) % 3][1])

            # 예측된 플레이어의 위치
            predict_plus = play_plus[0] + dxyz[i]
            predict_minus = play_minus[0] + dxyz[i]

            # 블록의 경계
            block_plus = (bxyz[i] + 50, bxyz[(i + 1) % 3] + 50, bxyz[(i + 2) % 3] + 50)
            block_minus = (bxyz[i] - 50, bxyz[(i + 1) % 3] - 50, bxyz[(i + 2) % 3] - 50)

            # 충돌 감지
            if check_overlap(block_minus[1], block_plus[1], play_minus[1], play_plus[1]) and \
               check_overlap(block_minus[2], block_plus[2], play_minus[2], play_plus[2]):
                if i in [0,1]:
                    if block_minus[0] < predict_plus < block_plus[0]:
                        result.append((i, 0))  # 양의 방향 충돌
                        k[i][0] = play_plus[0] - block_minus[0]
                    if block_minus[0] < predict_minus < block_plus[0]:
                        result.append((i, 1))  # 음의 방향 충돌
                        k[i][0] = play_minus[0] - block_plus[0]
                if i == 2:
                    if block_minus[0] < predict_plus < block_plus[0] or block_minus[0] < predict_minus < block_plus[0]:
                        if player.dz > 0:
                            result.append((i, 0)) #플레이어의 양의 방향 충돌
                            k[2][0] = abs(player.z - block_minus[0])
                        if player.dz < 0:
                            result.append((i, 1)) #플레이어의 음의 방향 충돌
                            k[2][1] = abs(player.z - block_plus[0])

    result2 = [[0,0],[0,0],[0,0]]
    for i in range(3):
        for j in range(2):
            if (i,j) in result:
                result2[i][j] = True
            else:
                result2[i][j] = False
    result2.append(k)
    return result2
def check_warp():
    global warp_working_count
    warp_block_list = map_loading.warp_block_list
    xyz = [player.x,player.y,player.z]
    
    if warp_working_count == 0:
        for block in map_loading.map_test.BLOCKS:
            if abs(xyz[0] - block.x) < 100:
                if abs(xyz[2] - block.z) < 100:
                    if block.texture_num == 9:
                        if warp_working_count == 0:
                            for i in range(0, len(warp_block_list)):
                                if block.x == warp_block_list[i][0] and block.y == warp_block_list[i][1] and block.z == warp_block_list[i][2]:
                                    if warp_working_count == 0:
                                        for j in range(0, len(warp_block_list)):
                                            if warp_block_list[j][3] == warp_block_list[i][3]:
                                                if j != i:
                                                    warp_working_count = 1
                                                    player.x = warp_block_list[j][0]
                                                    player.y = warp_block_list[j][1] - 100
                                                    player.z = warp_block_list[j][2]
                                                    camera_pos[0] = warp_block_list[j][0]
                                                    camera_pos[1] = warp_block_list[j][1]
                                                    break
                                    else:
                                        break
                        else:
                            break
    else:
        for i in range(0, len(warp_block_list)):
            
            if xyz[0] == warp_block_list[i][0] and xyz[1] == warp_block_list[i][1] - 100 and xyz[2] == warp_block_list[i][2]:
                break
        else:
            warp_working_count = 0

def adjust(k, i):
    if (0 < abs(k[i][0]) < abs(k[i][1])) or (abs(k[i][1])==0):
        if i == 0:
            player.x -= k[i][0]
        elif i == 1:
            player.y -= k[i][0]
        elif i == 2:
            player.z += k[i][0] -1
    elif (abs(k[i][0]) > abs(k[i][1]) > 0) or (abs(k[i][0])==0):
        if i == 0:
            player.x -= k[i][1]
        elif i == 1:
            player.y -= k[i][1]
        elif i == 2:
            player.z -= k[i][1] -1

#플레이어 움직임 실시간 적용
def player_during():
    print("\n\n\n\n\n\n\n")
    print (player.x,player.y,player.z)
    global delta_time
    player.ani = "stand"
    FPS = 1000
    delta_time = clock.tick(FPS) / 2
    if z_key_count == 0:
        x_col,y_col,z_col,k = check_collision()
        check_warp()
        if True not in x_col:
            player.x += player.dx * delta_time
        elif abs(player.dx) > 0:
            adjust(k, 0)
        x_col,y_col,z_col,k = check_collision()
        if True not in y_col:
            player.ani = "jump"
            player.y += player.dy * delta_time
            player.dy += GRAVITY
            player.jump_OK = False
        else:
            adjust(k, 1)
            player.dy = 1
            if y_col[0]:
                player.jump_OK = True
        x_col,y_col,z_col,k = check_collision()
        if True not in z_col and is_3D:
            player.z += player.dz * delta_time
        elif is_3D:
            adjust(k, 2)
        elif not is_3D:
            player.z = 100
        elif False not in z_col:
            adjust(k, 0)
            adjust(k, 1)
        if abs(player.z - player.fake_z) >= 5:
            if player.ani != "jump":
                player.ani = "walk"
            player.fake_z += 0.3 * delta_time * (player.z - player.fake_z)
        else:
            player.fake_z = player.z
        if abs(player.x - player.fake_x) >= 5:
            if player.ani != "jump":
                player.ani = "walk"
            player.fake_x += 0.3 * delta_time * (player.x - player.fake_x)
        else:
            player.fake_x = player.x


        
        
        
    elif z_key_count == 1:
        check_warp()
        player.fake_z = player.z
        player.fake_x = player.x


    player.points = [
        [player.fake_x - player.size, player.y - 3*player.size], [player.fake_x + player.size, player.y - 3*player.size],
        [player.fake_x + player.size, player.y + player.size], [player.fake_x - player.size, player.y + player.size],
    ]

    player.range = (player.fake_x-camera_pos[0])**2 + (player.y-50-camera_pos[1])**2 + (player.fake_z-camera_pos[2])**2

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

def draw_square(square,color_set):
    temp_square = []
    temp = 0
    for point in square[0:4]:
        temp_square.append(projection_3D.project_3d_or_2d((point[0],point[1],point[3]), camera_pos, angle_x, angle_y))
    square = temp_square
    if (None not in square):
        for point in square:
            if not (0 <= point[0] <= screen_width and 0 <= point[1] <= screen_height):
                temp += 1
            if temp == 4:
                return
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

def jump(pressed):
    if pressed == True:
        if z_key_count == 0:
            if player.jump_OK:
                player.dy = player.jump_power

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
                    player.dx -= player.speed
            
            if event.key == pygame.K_d:
                    player.dx += player.speed

            if event.key == pygame.K_w:#z축 앞 이동
                    player.dz += player.speed
                
            if event.key == pygame.K_s: #z축 뒤 이동
                    player.dz -= player.speed
            

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
                player.jump_pressed = True 

                    

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a: 
                player.dx += player.speed
                if z_key_count == 1:
                    player.x -= 100
                    camera_pos[0] -= 100
            if event.key == pygame.K_w:
                player.dz -= player.speed
                if z_key_count == 1:
                    player.z += 100
                    camera_pos[2] += 100
                    

                pass
            if event.key == pygame.K_d: 
                player.dx -= player.speed
                if z_key_count == 1:
                    player.x += 100
                    camera_pos[0] += 100
            if event.key == pygame.K_s: 
                player.dz += player.speed
                if z_key_count == 1:
                    player.z -= 100
                    camera_pos[2] -= 100

            if event.key == pygame.K_SPACE: 
                player.jump_pressed = False
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
    jump(player.jump_pressed)
def camera_move():
    # 부드럽게 이동
    global camera_pos, z_key_count
    
    if z_key_count == 0:
        for i in range(3):
            target_camera_pos = player.x,(player.y-300),(player.z - 800)
            camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * delta_time * 0.1


def block_3D_transition(blockk):
    global camera_pos
    
    # 부드럽게 이동
    
    if is_3D == False:
        blockk.z = 100
        for point in blockk.points:
        
            x, y = point[0],point[1]
            if(abs(100 - point[3])>10):
                point[3] += (100 - point[3]) * 0.2
            else:
                point[3] = 100
            z = point[3]

            point = x,y,point[2],z


    else:
        blockk.z = blockk.original_z
        for point in blockk.points:
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
        block_3D_transition(block)
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