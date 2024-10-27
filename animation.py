from settings import *


import pygame
import os
# 이미지 폴더에서 이미지들을 불러옴
walk_images = [f"walkanime/walk_{i}" for i in range(1, 4)]
jump_images = [f"jumpanime/jump_{i}" for i in range(1, 4)]
standing_images = ["standinganime//player"]

# 애니메이션 상태 변수 초기화
last_update = 0
current_frame = 0
img = standing_images  # 처음 상태는 idle 상태로 초기화


def anime():
    import real_game
    import Player
    import projection_3D
    player_x_d = real_game.player_x_d
    player_z_d = real_game.player_z_d
    player_y_VELOCITY = real_game.player_y_VELOCITY
    global last_update, current_frame, img
    
    if is_3D == False:
        temp = []
        for point in Player.playerblock.points:
            temp.append(projection_3D.project_3d_or_2d((point[0],point[1],point[3]), camera_pos,angle_x,angle_y))

    now = pygame.time.get_ticks()

    # 캐릭터의 상태에 따른 애니메이션 설정
    if player_x_d != 0 or player_z_d != 0:
        walking = True
        jumping = False
    elif player_y_VELOCITY != 0:
        walking = False
        jumping = True
    else:
        walking = False
        jumping = False

    # 상태에 따른 이미지 변경
    if walking:
        if now - last_update > 200:  # 200ms마다 이미지 변경
            last_update = now
            current_frame = (current_frame + 1) % len(walk_images)
            draw_quad(walk_images[current_frame], temp)
            print(walk_images[current_frame])
            print('바뀜')
    elif jumping:
        if now - last_update > 200:  # 200ms마다 이미지 변경
            last_update = now
            current_frame = (current_frame + 1) % len(jump_images)
            draw_quad(jump_images[current_frame], temp)
            
    else:
        if now - last_update > 50:  # 350ms마다 이미지 변경 (idle 상태)
            draw_quad(standing_images[0], temp)
            
#이중 적분 느낌? 선형 보간
def lerp( p1, p2, f ):
    return p1 + f * (p2 - p1)

def lerp2d( p1, p2, f ):
    return tuple( lerp( p1[i], p2[i], f ) for i in range(2) )

def draw_quad( image_name, quad ):
    img = pygame.image.load(f"{script_dir}//images//{image_name}.png").convert_alpha()

    points = dict()

    for i in range( img.get_size()[1]+1 ):
        b = lerp2d( quad[1], quad[2], i/img.get_size()[1] )
        c = lerp2d( quad[0], quad[3], i/img.get_size()[1] )
        for u in range( img.get_size()[0]+1 ):
            a = lerp2d( c, b, u/img.get_size()[0] )
            points[ (u,i) ] = a

    for x in range( img.get_size()[0] ):
        for y in range( img.get_size()[1] ):
            color = img.get_at((x,y))
            if color[3] > 0:  # 알파 값이 0이 아닌 경우만 그리기
                pygame.draw.polygon(
                    screen,
                    color,
                    [ points[ (a,b) ] for a, b in [ (x,y), (x,y+1), (x+1,y+1), (x+1,y) ] ] 
                )
#     draw_quad( "시작1", ( (300,300), (600,450), (600,600), (400,600) ))