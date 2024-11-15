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
import dead
from dialogue import *
from screen_effect import *
import settings
import dialogue
import random

overlap_message_timer = 0

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
    if texture_num != 8:
        map_loading.BLOCKS.append(map_loading.Block((nearestx_100,nearesty_100,nearestz_100),texture_num))
    if texture_num == 8:
        eventname = input("일어날 이벤트명을 작성해 주세요 : ")
        size = input("차원 균열의 크기는 몇배? : ")
        event_name_list.append(eventname)
        event_size_list.append(size)
        event_block_x_list.append(nearestx_100)
        event_block_y_list.append(nearesty_100)
        event_block_z_list.append(nearestz_100)

camera_shake_offset = [0, 0]

def swing():
    global camera_shake_offset
    if map_loading.stagename == "stage6":
        if piece.swinging == 1:
            shake_intensity = 20  # 흔들림 강도
            camera_shake_offset[0] = random.randint(-shake_intensity, shake_intensity)
            camera_shake_offset[1] = random.randint(-shake_intensity, shake_intensity)
        else:
            # 범위를 벗어나면 흔들림이 끝나고 오프셋 초기화
            camera_shake_offset = [0, 0]
        camera_pos[0] += camera_shake_offset[0]
        camera_pos[2] += camera_shake_offset[1]

def blockremove():
    nearestx_100 = round(player.x / 100) * 100
    nearesty_100 = round(player.y / 100) * 100 + 100
    nearestz_100 = round(player.z / 100) * 100
        
    block_to_remove = (nearestx_100, nearesty_100, nearestz_100)
    
    for block in map_loading.BLOCKS:
        if block.pos == block_to_remove:
            map_loading.BLOCKS.remove(block)
            break
            
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
    
    global warp_working_count, map_loading_count
    if z_key_count == 0:
        warp_block_list = map_loading.warp_block_list
        xyz = [player.x,player.y,player.z]

        if warp_working_count == 0:
            if map_loading_count == 1:
                for j in range(0, len(warp_block_list)):
                    if warp_block_list[j][3] == map_loading.stagename:
                        warp_working_count = 1
                        map_loading_count = 0
                        player.x = warp_block_list[j][0]
                        player.y = 4000
                        
                        player.z = warp_block_list[j][2]
                        camera_pos[0] = warp_block_list[j][0]
                        camera_pos[1] = warp_block_list[j][1] - 400
                        camera_pos[2] = warp_block_list[j][1] - 800
                    else:
                        pass
            else:
                for j in range(0, len(warp_block_list)):
                    if warp_block_list[j][3] == map_loading.stagename:
                        pass
                else:
                    for block in map_loading.BLOCKS:
                        
                        if abs(xyz[0] - block.x) < 100 and abs(xyz[2] - block.z) < 50 and -101 < (xyz[1] - block.y) < 201 and block.texture_num == 9:
                            for i in range(0, len(warp_block_list)):
                                modifiyed_map_name = int(map_loading.stagename[5]) + 1
                                modifiyed_map_name2 = map_loading.stagename[0:5] + str(modifiyed_map_name)
                                if warp_block_list[i][3] == modifiyed_map_name2:
                                    
                                    map_loading.map_load(modifiyed_map_name2)
                                    map_loading_count = 1                                    
                                else:
                                    if (
                                        block.x == warp_block_list[i][0]
                                        and block.y == warp_block_list[i][1]
                                        and block.z == warp_block_list[i][2]
                                    ):
                                        for j in range(0, len(warp_block_list)):
                                            if warp_block_list[j][3] == warp_block_list[i][3]:
                                                if j != i:
                                                    warp_working_count = 1

                                                    player.x = warp_block_list[j][0]
                                                    player.y = warp_block_list[j][1] - 100
                                                    player.z = warp_block_list[j][2]
                                                    camera_pos[0] = warp_block_list[j][0]
                                                    camera_pos[1] = warp_block_list[j][1] - 400
                                                    camera_pos[2] = warp_block_list[j][1] - 800
                                                    
                                                    break
                                        break
                            break
        else:
            for i in range(0, len(warp_block_list)):
                if (
                    abs(xyz[0] - warp_block_list[i][0]) < 100
                    and abs((xyz[1] - warp_block_list[i][1])) <= 150
                    and abs(xyz[2] - warp_block_list[i][2]) < 100
                ):
                    warp_working_count = 1
                    break
                    
            else:
                warp_working_count = 0

def adjust(k, i):
    if (0 < abs(k[i][0]) < abs(k[i][1])) or (abs(k[i][1])==0) and prevent2 == False:
        if i == 0:
            player.x -= k[i][0]
        elif i == 1:
            player.y -= k[i][0]
        elif i == 2:
            player.z += k[i][0] -1
    elif (abs(k[i][0]) > abs(k[i][1]) > 0) or (abs(k[i][0])==0) and prevent2 == False:
        if i == 0:
            player.x -= k[i][1]
        elif i == 1:
            player.y -= k[i][1]
        elif i == 2:
            player.z -= k[i][1] -1

#플레이어 움직임 실시간 적용

def player_during():
    global delta_time
    player.ani = "stand"
    
    
    FPS = 60
    delta_time = clock.tick(FPS)/10
    if z_key_count == 0:
        
        x_col,y_col,z_col,k = check_collision()
        check_warp()
        if True not in x_col and prevent2 == False:
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
        if True not in z_col and is_3D and prevent2 == False:
            player.z += player.dz * delta_time
        elif is_3D:
            adjust(k, 2)
        elif not is_3D:
            player.z = 100
        elif False not in z_col:
            adjust(k, 0)
            adjust(k, 1)
        if abs(player.z - player.fake_z) >= 5:
            player.ani = "zwalk"
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
        player.dy = 1
        player.fake_z = player.z
        player.fake_x = player.x


    player.points = [
        [player.fake_x - player.size, player.y - 3*player.size], [player.fake_x + player.size, player.y - 3*player.size],
        [player.fake_x + player.size, player.y + player.size], [player.fake_x - player.size, player.y + player.size],
    ]

    player.up_range = (player.fake_x-camera_pos[0])**2 + (player.y-100-camera_pos[1])**2 + (player.fake_z-10-camera_pos[2])**2
    player.down_range = (player.fake_x-camera_pos[0])**2 + (player.y-camera_pos[1])**2 + (player.fake_z-10-camera_pos[2])**2
    player.y = round(player.y)


    
    
# 큐브의 면을 그리는 함수


def draw_square(square,color_set):
    global last_update, now
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
        pygame.draw.aalines(screen, color_set[1], True, square, True)
        # pygame.draw.lines(screen, color_set[1], True, square, 4)
        # pygame.draw.polygon(screen, color_set[1], square, 1)  # 테두리 두께 4
       

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
# def mouse_rotate_check():
#     if prevent == True:
#         return
#     global angle_x, angle_y
#     mouse_dx, mouse_dy = pygame.mouse.get_rel()

#     # 각도 업데이트 (마우스 이동에 따라)

#     angle_x += mouse_dx * mouse_sensitivity
#     if (-math.pi/2<angle_y + mouse_dy * mouse_sensitivity<math.pi/2):
#         angle_y += mouse_dy * mouse_sensitivity
wheep_sound = pygame.mixer.Sound("music/차원변환.mp3")
def event_check():
    global condition, is_3D, overlap_message_timer,target_camera_pos, color, z_key_count, texture_num, m_key_count, last_update, h_key_count, patterns, nowtime, next_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if pygame.K_0 <= event.key <= pygame.K_9:
                texture_num = event.key - pygame.K_0
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_z: #개발자 모드 실행
                if z_key_count == 0:
                    z_key_count = 1
                    color = 255                    
                else:
                    z_key_count = 0
                    color = 0
            if event.key == pygame.K_k:
                if z_key_count == 1:
                    print(player.x , player.y, player.z)
            if event.key == pygame.K_p: # 맵 세이브
                if (z_key_count == 1 and is_3D) or map_loading.stagename == "stage1":
                    map_loading.map_save()
            if event.key == pygame.K_l: # 맵 로딩
                if z_key_count == 1:
                    map_loading.map_load("")
            if event.key == pygame.K_SPACE:
                player.jump_pressed = True 
            if event.key == pygame.K_m:
                if m_key_count == 0:
                    m_key_count = 1
                    last_update = pygame.time.get_ticks()
                    reset_block_timers()
                    print("m 키 눌림 - 타이머 시작")                  
                else:
                    m_key_count = 0
            # if event.key == pygame.K_h:
            #     h_key_count +=1
            #     patterns.append(pattern.Pattern(f"pattern{h_key_count}"))
                
                

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a: 
                player.dx = 0
                if z_key_count == 1:
                    player.x -= 100
                    camera_pos[0] -= 100
            if event.key == pygame.K_w:
                player.dz = 0
                if z_key_count == 1:
                    player.z += 100
                    camera_pos[2] += 100
                    

                pass
            if event.key == pygame.K_d: 
                player.dx = 0
                if z_key_count == 1:
                    player.x += 100
                    camera_pos[0] += 100
            if event.key == pygame.K_s: 
                player.dz = 0
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


        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 3:
                if z_key_count == 1:    
                    setblock(texture_num)
                
            elif event.button == 2:
                if z_key_count == 1:    
                    blockremove()
            elif event.button == 1 and prevent2 == False and int(map_loading.stagename[5]) in [5,6,7] and piece.cantR == 0:
                if int(map_loading.stagename[5]) == 7:
                    if piece.core_in:
                        piece.core_hp += 1
                    return
                        
                # 시점 전환 목표 설정
                if is_3D:
                    temp = 0
                    for block in map_loading.BLOCKS:
                        if abs(block.x - player.x) < 100 and -100 < (player.y - block.y) < 200:
                            temp += 1
                    if temp == 0:
                        if piece.core_in:
                            piece.core_hp += 1
                        is_3D = False
                        wheep_sound.set_volume(2)
                        wheep_sound.play()
                    else :
                        overlap_message_timer = 60
                elif not is_3D:
                    temp = []
                    for block in map_loading.BLOCKS:
                        if abs(block.x - player.x) < 100:
                            temp.append(block.original_z)
                    if not temp:
                        player.z = 100
                    else: 
                        player.z = min(temp)
                    
                    is_3D = True
                    wheep_sound.set_volume(2)
                    wheep_sound.play()

    jump(player.jump_pressed)

    pygame.event.clear()
    keys = pygame.key.get_pressed()
    player.dz = 0
    player.dx = 0
    
    if keys[pygame.K_w]:
        player.dz = player.speed
    if keys[pygame.K_a]:
        player.dx = -player.speed
    if keys[pygame.K_s]:
        player.dz = -player.speed
    if keys[pygame.K_d]:
        player.dx = player.speed
    if keys[pygame.K_a] and keys[pygame.K_d]:
        player.dx = 0
    if keys[pygame.K_w] and keys[pygame.K_s]:
        player.dz = 0
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    
    
    
def camera_move():
    if prevent == True:
        return
    # 부드럽게 이동
    global camera_pos, z_key_count

    if z_key_count == 0:
        for i in range(3):
            target_camera_pos = player.x,(player.y-(800*math.sin(angle_y))),(player.z - (800*math.cos(angle_y)))
            camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.5


#보스전 기믹~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 보스전 기믹 관련 코드
        

def add_block_action(x, y, z):
    # 동일 위치에서 중복 작업을 추가하지 않도록 하기
    for action in block_action_queue:
        if action["position"] == (x, y, z):
            return  # 이미 해당 위치에 대한 액션이 존재하면 추가하지 않음
    # 각 블록 작업이 독립적인 타이머와 상태를 갖도록 함
    block_action_queue.append({
        "position": (x, y, z), 
        "status": "pending_removal_2", 
        "timer": 0,
        "texture_num": 0
    })
    
def reset_block_timers():
    # m 키를 누른 순간 타이머를 초기화하여 새로 시작하게 함
    for action in block_action_queue:
        action["timer"] = 0

def disable_block_timers():
    global m_key_count, block_action_queue
    m_key_count = 0
    for action in block_action_queue:
        if action["status"] == "removed":
            x, y, z = action["position"]
            try:
                map_loading.BLOCKS.append(map_loading.Block((x, y, z), 0))
            except:
                print("블록을 다시 생성하는 중 오류가 발생했습니다.")
        elif action["status"] == "pending_removal":
            x, y, z = action["position"]
            try:
                for block in map_loading.BLOCKS:
                    if block.pos == (x, y, z) and block.texture_num == 1:
                        map_loading.BLOCKS.remove(block)
                        break
                map_loading.BLOCKS.append(map_loading.Block((x, y, z), 0))
            except:
                print("블록을 다시 생성하는 중 오류가 발생했습니다.")
    
    block_action_queue.clear()

def block_break_and_create():
    global block_action_queue, last_update, m_key_count
    time_delta = nowtime - last_update
    last_update = nowtime
    
    if prevent:
        disable_block_timers()
        
    for action in list(block_action_queue):
        if m_key_count == 1 and is_talking == False:
            action["timer"] += time_delta

        # 블록 삭제 처리 (1.5초 후)
        if action["status"] == "pending_removal" and action["timer"] >= 1000:
            x, y, z = action["position"]
            try:
                for block in map_loading.BLOCKS:
                    if block.pos == (x, y, z):
                        map_loading.BLOCKS.remove(block)
                        action["timer"] = 0
                        action["status"] = "removed"
            except:
                # 이미 지워진 블록임
                pass
        elif action["status"] == "pending_removal_2" and action["timer"] >= 500:
            x, y, z = action["position"]
            try:
                for block in map_loading.BLOCKS:
                    if block.pos == (x, y, z):
                        map_loading.BLOCKS.remove(block)
                        map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
                        action["timer"] = 0
                        action["status"] = "pending_removal"
            except:
                pass
        # elif action["status"] == "removed" and action["timer"] >= 1500:
        #     x, y, z = action["position"]
        #     texture = action["texture_num"]
        #     try:
        #         map_loading.BLOCKS.append(map_loading.Block((x, y, z), texture))
        #         block_action_queue.remove(action)
        #     except:
        #         print("이미 생성")
                
                
    
# 플레이어 위치에 따른 블록 액션 추가
def handle_player_action():
    nearestx_100 = round(player.x / 100) * 100
    nearesty_100 = round(player.y / 100) * 100 + 100
    nearestz_100 = round(player.z / 100) * 100

    # 현재 플레이어 위치에 블록 액션 추가
    add_block_action(nearestx_100, nearesty_100, nearestz_100)


def block_3D_transition(block):
    global camera_pos
    
    # 부드럽게 이동
    
    if is_3D == False: #2D
        block.z = 100
        for point in block.points:
        
            x, y = point[0],point[1]
            if(abs(100 - point[3])>10):
                point[3] += (100 - point[3]) * 0.3
            else:
                point[3] = 100
            z = point[3]

            point = x,y,point[2],z


    else:
        block.z = block.original_z
        for point in block.points:
            x, y = point[0],point[1]
            if(abs(point[2] - point[3])>10):
                point[3] += (point[2] - point[3]) * 0.3
            else:
                point[3] = point[2]
            z = point[3]

            point = x,y,point[2],z


def pattern_looping():
    import pattern
    global last_time, cur_pattern, patterns, flag
    print (cur_pattern)
    if flag == True:
        pattern.reloadpattern()
        flag = False
    if (time.time() - last_time) > pattern.pattern_loop[cur_pattern][1]:
        last_time = time.time()
        cur_pattern += 1
        if cur_pattern >= len(pattern.pattern_loop ):
            cur_pattern = 1
            pattern.reloadpattern()
        patterns.append(pattern.pattern_loop[cur_pattern][0])


def draw_health_bar():
    bar_width = 200
    bar_height = 30
    bar_x = (1200 - bar_width) // 2
    bar_y = 50
    
    # 배경 바 그리기
    pygame.draw.rect(screen, (169, 169, 169), (bar_x, bar_y, bar_width, bar_height))

    # 체력에 해당하는 빨간색 바 채우기
    filled_width = int((piece.core_hp / 200) * bar_width)
    pygame.draw.rect(screen, (0, 255, 255), (bar_x, bar_y, filled_width, bar_height))

    # 줄어든 부분을 검은색으로 표시
    if filled_width < bar_width:
        pygame.draw.rect(screen, BLACK, (bar_x + filled_width, bar_y, bar_width - filled_width, bar_height))

    # 텍스트 표시
    font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 24)
    text = font.render(f"{piece.core_hp} / 200", True, WHITE)
    text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
    screen.blit(text, text_rect)

    # '에너지 코어' 텍스트 표시
    title_font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 28)  # 제목 크기 더 크게 설정
    title_text = title_font.render("에너지 코어", True, BLACK)
    title_text_rect = title_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 20))  # 바 위쪽에 위치
    screen.blit(title_text, title_text_rect)
    

def draw_order_cal():
    if (is_3D):
        piece.cal_range()
        for one_piece in piece.Pieces:
            one_piece.drawed = False
        global drawed_player_up,drawed_player_down
        drawed_player_up = False
        drawed_player_down = False
        for square in showing.squares:
            piece.draw_real_piece(square[5])
            if player.up_range > square[5] and drawed_player_up == False:
                drawed_player_up = True
                animation.anime("up")
            if player.down_range > square[5] and drawed_player_down == False:
                drawed_player_down = True
                animation.anime("down")
            draw_square(square[0:4],square[4])
        for one_piece in piece.Pieces:
            if one_piece.drawed == False:
                piece.forced_draw(one_piece)
        if drawed_player_up == False:
            animation.anime("up")
        if drawed_player_down == False:
            animation.anime("down")
    else:
        piece.cal_range()
        for square in showing.squares_front:
            draw_square(square[0:4],square[4])
        for one_piece in piece.Pieces:
            piece.forced_draw(one_piece)
        animation.anime("up")
        animation.anime("down")
    if extend_piece and map_loading.stagename == "stage6":
        for piece1 in piece.Pieces:
            if piece1.event == "stage7":
                piece1.size = 0
        if dialogue.extend_modified_size < 8000:
            dialogue.extend_modified_size *= 1.03
            dialogue.extend_piece_pos[0] += 0.01 * (600 - dialogue.extend_piece_pos[0])
            dialogue.extend_piece_pos[1] += 0.01 * (400 - dialogue.extend_piece_pos[1])
            print (dialogue.extend_modified_size)
            modified_img = pygame.transform.scale(piece.Pieces[0].img, (dialogue.extend_modified_size,dialogue.extend_modified_size))
            modified_rect = modified_img.get_rect()
            modified_width, modified_height = modified_rect.width, modified_rect.height

            screen.blit(modified_img, (dialogue.extend_piece_pos[0] - (modified_width / 2), dialogue.extend_piece_pos[1] - (modified_height / 2)))
        else:
            screen.fill((10, 10, 10))

current_music = None    
def play_stage_music(stagename):
    global current_music
    
    # stage 삭제후 정수만 넣기
    try:
        stage_number = int(stagename.replace("stage", ""))
    except ValueError:
        return 

    if stage_number in [1, 2, 3]:
        music_file = "music/123.mp3"
    elif stage_number in [4, 5, 6]:
        music_file = "music/456.mp3"
    elif stage_number == 7:
        music_file = "music/보스전.mp3"
    if dialogue.current_dialogue_key == "7-1":
        pygame.mixer.music.stop()
    
    if music_file and music_file != current_music:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # -1은 무한 반복
        pygame.mixer.music.set_volume(0.5)
        current_music = music_file  


puzzle = 0

def stage6_puzzle():
    global puzzle
    if map_loading.stagename == "stage6":
        if 150 < player.x < 250 and player.y == -400 and puzzle == 0:
            map_loading.show_saveblocks()
            puzzle += 1
def error404():
    global overlap_message_timer
    if overlap_message_timer > 0:
        font = pygame.font.Font("fonts/BMDOHYEON_otf.otf", 36)
        # Calculate alpha based on remaining frames
        alpha = int(255 * (overlap_message_timer / 60))
        text_surface = font.render("겹치는 블록 있음!", True, (255, 0, 0))
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (1200 - text_surface.get_width() - 10, 10))
        overlap_message_timer -= 1 


def draw_screen():
    global block, fade_opacity
    screen.fill((255, 255, 255))

    showing.squares = []
    showing.squares_front = []

    for block in map_loading.BLOCKS:
        block_3D_transition(block)
        check_cube(block.points, block.texture)
    
    showing.squares = sorted(showing.squares, key=lambda square: -square[5])
    piece.piece_3D_transition()
    draw_order_cal()
    if map_loading.stagename == "stage7":
        draw_health_bar()
    dead.player_dead_check()
    screen_effect(settings.scr_effect)
    draw_dialogue()
    error404()

    if dialogue.current_dialogue_key == "7-1":
        fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        fade_surface.fill((255, 255, 255))
        fade_surface.set_alpha(dialogue.fade_opacity)
        screen.blit(fade_surface, (0, 0))  

    pygame.display.flip()
    clock.tick(60)

def run():
    global condition, patterns, nowtime, fade_opacity
    nowtime = pygame.time.get_ticks()
    condition = "real_game"
    talkcheck()
    # print(start_looping_bool)
    if settings.start_looping_bool == True:
        pattern_looping()
        
    check_player_position()
    swing()
    if dialogue.is_talking == False:
        block_break_and_create()
    if (extend_piece and map_loading.stagename == "stage6") == False:
        
        event_check()
        player_during()
        camera_move()
        if map_loading.stagename == "stage6":
            stage6_puzzle()

    draw_screen()
    player_first_start()
    play_stage_music(map_loading.stagename)

    if m_key_count == 1:
        handle_player_action()

    for pattern_instance in patterns:
        import pattern
        if piece.core_hp < 30:
            pattern.start_pattern(pattern_instance)

    if dialogue.current_dialogue_key == "7-1" and dialogue.fade_opacity < 255:
        dialogue.fade_opacity += 5 
        if dialogue.fade_opacity >= 255:
            condition = "ending" 

    return condition
