import math
from player import *
from settings import *
import map_loading


def player_dead_check():
    import real_game
    real_game.prevent = False
    if player.y > 1000 :
        real_game.prevent = True
        tan_value = (real_game.camera_pos[1] - player.y +100) / (player.z - real_game.camera_pos[2])
        angle_radians = math.atan(tan_value)
        real_game.angle_x = 0
        real_game.angle_y = -angle_radians
        real_game.camera_pos[0] = player.fake_x
        

    if player.y > 1500 :
        padding =  int(player.y / 10 - 150)
        draw_speed = 4

        pygame.draw.line(screen, (0,0,0), (0,0), (0,screen_height), draw_speed * int(1.5 * padding))
        pygame.draw.line(screen, (0,0,0), (screen_width,0), (screen_width,screen_height), draw_speed * int(1.5 * padding))
        pygame.draw.line(screen, (0,0,0), (0,0), (screen_width,0), draw_speed * padding)
        pygame.draw.line(screen, (0,0,0), (0,screen_height), (screen_width,screen_height), draw_speed * padding)
        if (draw_speed * padding > 800) :
            player.x , player.y, player.z = (100,0,-500)
            real_game.target_camera_pos = [100, 0, -700]
            real_game.prevent = False
            real_game.angle_x,real_game.angle_y = (0,0)
        #각 스테이지의 플레이어 설정 좌표에 소환하기
