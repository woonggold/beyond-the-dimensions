import pygame   
import os
import collections
script_dir = os.path.dirname(__file__)

pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Beyond the Dimensions')
pygame.display.set_icon(pygame.image.load(f'{script_dir}/images/002.png'))

next_time = 0
camera_pos = [100, 0, -700]
camera_speed = 25  # 카메라 이동 속도
is_3D = False
target_camera_pos = camera_pos # 목표 카메라 위치
script_dir = os.path.dirname(__file__)

delta_time = clock.tick(60) / 10
angle_x, angle_y = 0, 0.245

mouse_sensitivity = 0.003

map_loading_count  =0

cube_size = 50

class Showing():
    def __init__(self):
        self.squares_front = []
        self.squares = []

showing = Showing()
extend_piece = False

block_textures = [[(255,255,255),(200,200,200),(100,100,100),(100,100,100)],\
                  [(255,0,0),(200,0,0),(100,0,0),(100,0,0)],\
                  [(0,255,255),(0,200,200),(0,100,100),(0,100,100)],\
                  [(0,255,0),(0,200,0),(0,100,0),(0,100,0)],\
                  [(240,240,255),(185,185,200),(85,85,100),(85,85,100)],\
                  [(0,0,255),(255,0,0),(0,0,0),(0,0,255)],\
                  [(255,0,0),(0,0,255),(0,255,0),(0,0,0)],\
                  [(0,255,0),(0,255,0),(0,255,0),(0,0,0)],\
                  [(0,0,255),(255,0,0),(0,255,0),(0,0,0)],\
                  [(255,255,0),(200,200,0),(100,100,0),(100,100,0)]] # 각각 0번부터 9번까지의 윗면, 옆면, 아랫면, 테두리의 색

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
m_key_count = 0
h_key_count = 0

#틱

# 각 작업을 저장할 큐 (순차적으로 삭제 및 생성 작업을 처리)
block_action_queue = collections.deque()



timer = 0

#블록 설치
blocks = []

prevent = False
prevent2 = False

scr_effect = "normal"

#첫번쨰 시작
firt_count = 0

#보스전 관련
#during용
count_second = 0
last_update = 0
last_update2 = 0
waitbool = False

patterns = []


cur_pattern = 0
last_time = 0
pattern_loop = []
flag = True
start_looping_bool = False

map_setting = [False, False, True, True, True, False, True]#순서대로 각 스테이지의 초기 is_3D 값.

def player_first_start():
    global firt_count, patterns
    if firt_count == 0:
        import map_loading, real_game, player
        
        if len(map_loading.warp_block_list) > 0:
            for i in range(0, len(map_loading.warp_block_list)):
                if map_loading.warp_block_list[i][3] == map_loading.stagename:
                    real_game.warp_working_count = 1
                    player.player.x , player.player.y, player.player.z = map_loading.warp_block_list[i][0] ,4000, map_loading.warp_block_list[i][2]
                    real_game.target_camera_pos = [map_loading.warp_block_list[i][0] ,map_loading.warp_block_list[i][1]-400, map_loading.warp_block_list[i][2] - 800]
        firt_count = 1 
        # real_game.cur_pattern = 0
        # patterns = []
        screen.fill((0, 0, 0))