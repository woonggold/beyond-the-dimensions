import pygame   
import os 
pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

camera_pos = [100, 0, -700]
camera_speed = 25  # 카메라 이동 속도
is_3D = False
target_camera_pos = camera_pos # 목표 카메라 위치
script_dir = os.path.dirname(__file__)

delta_time = clock.tick(60) / 10
angle_x, angle_y = 0, 0.245

map_name = "test"#이 map name을 변경해서 맵을 변경할 수 있음

mouse_sensitivity = 0.003

map_loading_count  =0

cube_size = 50

first_map_loading = 0

class Showing():
    def __init__(self):
        self.squares_front = []
        self.squares = []

showing = Showing()

block_textures = [[(100,100,100),(255,255,255),(0,0,0),(0,0,0)],\
                  [(0,255,0),(255,255,255),(0,0,0),(0,0,0)],\
                  [(0,255,255),(0,255,255),(0,255,255),(255,255,255)],\
                  [(0,0,0),(0,0,0),(0,0,0),(255,255,255)],\
                  [(0,255,0),(0,0,0),(0,255,0),(0,0,0)],\
                  [(0,0,255),(255,0,0),(0,0,0),(0,0,255)],\
                  [(255,0,0),(0,0,255),(0,255,0),(0,0,0)],\
                  [(0,255,0),(0,255,0),(0,255,0),(0,0,0)],\
                  [(0,0,255),(255,0,0),(0,255,0),(0,0,0)],\
                  [(0,0,0),(0,0,0),(0,0,0),(0,0,0)]] # 각각 0번부터 9번까지의 윗면, 옆면, 아랫면, 테두리의 색

GRAVITY = 2.35

warp_name_list = []
warp_block_x_list = []
warp_block_y_list = []
warp_block_z_list = []



warp_block_data = {
    "x": warp_block_x_list,
    "y": warp_block_y_list,
    "z": warp_block_z_list, 
    "warp_name": warp_name_list, 
}

event_name_list = []
event_size_list = []
event_block_x_list = []
event_block_y_list = []
event_block_z_list = []

event_block_data = {
    "x": event_block_x_list,
    "y": event_block_y_list,
    "z": event_block_z_list, 
    "event_name": event_name_list, 
    "size"  : event_size_list
}

aquire_piece_count = 0
texture_num = 0
warp_working_count = 0

#색칠 변수
color = 0

#키 누름 카운트
z_key_count =0

#블록 설치
blocks = []

prevent = False
prevent2 = False

scr_effect = "normal"

#첫번쨰 시작
firt_count = 0

def player_first_start():
    global firt_count
    if firt_count == 0:
        import map_loading, real_game, player
        
        if len(map_loading.warp_block_list) > 0:
            for i in range(0, len(map_loading.warp_block_list)):
                if map_loading.warp_block_list[i][3] == map_loading.stagename:
                    real_game.warp_working_count = 1
                    player.player.x , player.player.y, player.player.z = map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1] -100, map_loading.warp_block_list[i][2]
                    real_game.target_camera_pos = [map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1]-400, map_loading.warp_block_list[i][2] - 800]
        firt_count = 1 
        

map_setting = [False, True, True, True, True]#순서대로 각 스테이지의 초기 is_3D 값.
