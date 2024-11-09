from settings import *
from player import *

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


def anime(updown):
    import real_game
    import projection_3D
    global last_update, current_frame, img
    
    temp = []
    for point in player.points:
        temp.append(projection_3D.project_3d_or_2d((point[0],point[1],player.fake_z), camera_pos,real_game.angle_x,real_game.angle_y))
    if None in temp:
        return
    
    now = pygame.time.get_ticks()




    # 상태에 따른 이미지 변경
    if player.ani == "walk":
        if now - last_update > 200:  # 200ms마다 이미지 변경
            last_update = now
            current_frame = (current_frame + 1) % len(walk_images)
            player.image = walk_images[current_frame]
    elif player.ani == "jump":
        if now - last_update > 200:  # 200ms마다 이미지 변경
            last_update = now
            current_frame = (current_frame + 1) % len(jump_images)
            player.image = jump_images[current_frame]
            
    elif player.ani == "stand":
        if now - last_update > 50:  # 350ms마다 이미지 변경 (idle 상태)
            player.image = standing_images[0]
    draw_quad(player.image, temp, updown)
            
#이중 적분 느낌? 선형 보간
def lerp( p1, p2, f ):
    return p1 + f * (p2 - p1)

def lerp2d( p1, p2, f ):
    return tuple( lerp( p1[i], p2[i], f ) for i in range(2) )

def draw_quad( image_name, quad, updown):
    img = pygame.image.load(f"{script_dir}//images//{image_name}.png").convert_alpha()

    points = dict()

    for i in range( img.get_size()[1]+1 ):
        b = lerp2d( quad[1], quad[2], i/img.get_size()[1] )
        c = lerp2d( quad[0], quad[3], i/img.get_size()[1] )
        for u in range( img.get_size()[0]+1 ):
            a = lerp2d( c, b, u/img.get_size()[0] )
            points[ (u,i) ] = a


    if updown == "up":
        y_range = range(int(img.get_size()[1]/2)+1)
    if updown == "down":
        y_range = range(int(img.get_size()[1]/2)-1,img.get_size()[1])
    
    for x in range( img.get_size()[0] ):
        for y in y_range:
            color = img.get_at((x,y))
            if color[3] > 0:  # 알파 값이 0이 아닌 경우만 그리기
                pygame.draw.polygon(
                    screen,
                    color,
                    [ points[ (a,b) ] for a, b in [ (x,y), (x,y+1), (x+1,y+1), (x+1,y) ] ] 
                )
#     draw_quad( "시작1", ( (300,300), (600,450), (600,600), (400,600) ))