import math
from player import *
from settings import *
import map_loading
import time

stun_time = 0

def player_dead_check():
    global stun_time
    import real_game
    real_game.prevent2 = False
    delta_time = stun_time - time.time()
    if delta_time > 0:
        pygame.draw.line(screen, (0,0,0), (0,0), (0,screen_height), int(delta_time * 2400))
        pygame.draw.line(screen, (0,0,0), (screen_width,0), (screen_width,screen_height), int(delta_time * 2400))
        pygame.draw.line(screen, (0,0,0), (0,0), (screen_width,0), int(delta_time * 1600))
        pygame.draw.line(screen, (0,0,0), (0,screen_height), (screen_width,screen_height), int(delta_time * 1600))
        real_game.prevent2 = True
        tan_value = (real_game.camera_pos[1] - player.y +100) / (player.z - real_game.camera_pos[2])
        angle_radians = math.atan(tan_value)
        real_game.angle_x = 0
        real_game.angle_y = -angle_radians
        
    
    
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
            if len(map_loading.warp_block_list) > 0:
                for i in range(0, len(map_loading.warp_block_list)):
                    if map_loading.warp_block_list[i][3] == "stage2":
                        real_game.warp_working_count = 1
                        player.x , player.y, player.z = map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1] -100, map_loading.warp_block_list[i][2]
                        real_game.target_camera_pos = [map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1], map_loading.warp_block_list[i][2] - 200]
            else:
                player.x , player.y, player.z = 100,0,-500
                real_game.target_camera_pos = [100 ,0, -700]
            real_game.prevent = False
            real_game.angle_x,real_game.angle_y = (0,0)
            player.dy = 0
            stun_time = time.time() + 0.5
        #각 스테이지의 플레이어 설정 좌표에 소환하기
