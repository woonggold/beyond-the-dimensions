import math, time
from player import *
from settings import *
import map_loading, piece

stun_time = 0

def player_dead_check():
    global stun_time
    import real_game
    delta_time = stun_time - time.time()
    if delta_time < 0:
        real_game.angle_x = 0
        mouse_dy = pygame.mouse.get_rel()[1]
        if (-math.pi/2<real_game.angle_y + mouse_dy * mouse_sensitivity<math.pi/2) and real_game.prevent2 == False:
            real_game.angle_y += mouse_dy * mouse_sensitivity
    real_game.prevent2 = False
        
    if delta_time > 0:
        pygame.draw.line(screen, (0,0,0), (0,0), (0,screen_height), int(delta_time * 2400))
        pygame.draw.line(screen, (0,0,0), (screen_width,0), (screen_width,screen_height), int(delta_time * 2400))
        pygame.draw.line(screen, (0,0,0), (0,0), (screen_width,0), int(delta_time * 1600))
        pygame.draw.line(screen, (0,0,0), (0,screen_height), (screen_width,screen_height), int(delta_time * 1600))
        real_game.prevent2 = True
        real_game.angle_x = 0
        real_game.angle_y = 0
        
    
    
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
        if (draw_speed * padding > 800) : #ㄹㅇ 죽음
            if len(map_loading.warp_block_list) > 0:
                for i in range(0, len(map_loading.warp_block_list)):
                    if map_loading.warp_block_list[i][3] == map_loading.stagename:
                        real_game.warp_working_count = 1
                        player.x , player.y, player.z = map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1] -100, map_loading.warp_block_list[i][2]
                        real_game.target_camera_pos = [map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1]-400, map_loading.warp_block_list[i][2] - 800]
            else:
                player.x , player.y, player.z = 100,0,-500
                real_game.target_camera_pos = [100 ,-300, -1300]
            piece.Pieces = []
            if "event_blocks" in map_loading.data:
                for i in range(0, len(map_loading.data["event_blocks"]["x"])):
                    piece.Pieces.append(piece.MakePiece((map_loading.data["event_blocks"]["x"][i],map_loading.data["event_blocks"]["y"][i],map_loading.data["event_blocks"]["z"][i]),map_loading.data["event_blocks"]["event_name"][i],map_loading.data["event_blocks"]["size"][i]))
                    event_block_x_list.append(map_loading.data["event_blocks"]["x"][i])
                    event_block_y_list.append(map_loading.data["event_blocks"]["y"][i])
                    event_block_z_list.append(map_loading.data["event_blocks"]["z"][i])
                    event_name_list.append(map_loading.data["event_blocks"]["event_name"][i])
                    event_size_list.append(map_loading.data["event_blocks"]["size"][i])
            real_game.prevent = False
            real_game.angle_x,real_game.angle_y = (0,0)
            player.dy = 0
            stun_time = time.time() + 0.5
            real_game.is_3D = map_setting[int(map_loading.stagename[5])-1] #맵의 초기 is_3D값을 초기화해주는 코드임.
