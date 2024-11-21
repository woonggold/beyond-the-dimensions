from settings import *
from player import *

import pygame
import os
import real_game

# 이미지 폴더에서 이미지들을 불러옴
walk_images = [f"walkanime/walkXAxis_{i}" for i in range(1, 7)]
zwalk_images = [f"walkanime/walkYAxis_{i}" for i in range(1, 6)]
jump_images = [f"jumpanime/jump_{i}" for i in range(1, 5)]
standing_images = ["standinganime//player"]

# 애니메이션 상태 변수 초기화
last_update = 0
current_frame = 0
img = standing_images  # 처음 상태는 idle 상태로 초기화
walk_sound = pygame.mixer.Sound("music/walking.mp3")
walk_sound.set_volume(2)
walk_sound_played = False

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
        global walk_sound_played
        if not walk_sound_played:  # 효과음이 아직 재생되지 않은 경우
            walk_sound.play()
            walk_sound_played = True
        if now - last_update > 50:  # 워크는 좀빨리
            last_update = now
            current_frame = (current_frame + 1) % len(walk_images)
            player.image = walk_images[current_frame]
    elif player.ani == "zwalk":
        if not walk_sound_played:  # 효과음이 아직 재생되지 않은 경우
            walk_sound.play()
            walk_sound_played = True
        if now - last_update > 50:  # 워크는 좀빨리
            last_update = now
            current_frame = (current_frame + 1) % len(zwalk_images)
            player.image = zwalk_images[current_frame]
    elif player.ani == "jump":
        walk_sound.stop()
        walk_sound_played = False
        if now - last_update > 100:  # 점프는 100ms정도
            last_update = now
            current_frame = (current_frame + 1) % len(jump_images)
            player.image = jump_images[current_frame]
            
    elif player.ani == "stand":
        walk_sound.stop()
        walk_sound_played = False
        if now - last_update > 50:  # 350ms마다 이미지 변경 (idle 상태)
            player.image = standing_images[0]
    draw_quad(player.image, temp, updown)
            
#이중 적분 느낌? 선형 보간
def lerp( p1, p2, f ):
    return p1 + f * (p2 - p1)

def lerp2d( p1, p2, f ):
    return tuple( lerp( p1[i], p2[i], f ) for i in range(2) )

def draw_quad(image_name, quad, updown):
    # 이미지를 로드
    img = pygame.image.load(f"{script_dir}//images//{image_name}.png").convert_alpha()

    # `player.dx`가 음수일 때 이미지를 좌우 반전
    if player.ani == "walk" and player.dx < 0:
        img = pygame.transform.flip(img, True, False)
    if player.ani == "jump" and real_game.nowA == True:
        img = pygame.transform.flip(img, True, False)
    # 나머지 코드는 그대로
    points = dict()

    for i in range(img.get_size()[1] + 1):
        b = lerp2d(quad[1], quad[2], i / img.get_size()[1])
        c = lerp2d(quad[0], quad[3], i / img.get_size()[1])
        for u in range(img.get_size()[0] + 1):
            a = lerp2d(c, b, u / img.get_size()[0])
            points[(u, i)] = a

    if updown == "up":
        y_range = range(int(img.get_size()[1] / 2) + 1)
    elif updown == "down":
        y_range = range(int(img.get_size()[1] / 2) - 1, img.get_size()[1])

    for x in range(img.get_size()[0]):
        for y in y_range:
            color = img.get_at((x, y))
            if color[3] > 0:  # 알파 값이 0이 아닌 경우만 그리기
                pygame.draw.polygon(
                    screen,
                    color,
                    [points[(a, b)] for a, b in [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]]
                )
#     draw_quad( "시작1", ( (300,300), (600,450), (600,600), (400,600) ))