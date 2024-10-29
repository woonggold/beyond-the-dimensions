import pygame   
import os 
pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

camera_pos = [0, 0, -1000]
camera_speed = 25  # 카메라 이동 속도
is_3D = False
target_camera_pos = camera_pos # 목표 카메라 위치
script_dir = os.path.dirname(__file__)

angle_x, angle_y = 0, 0

map_name = "test"#이 map name을 변경해서 맵을 변경할 수 있음

mouse_sensitivity = 0.003

cube_size = 50

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
                  [(255,255,255),(255,255,255),(255,255,255),(255,255,255)]] # 각각 0번부터 9번까지의 윗면, 옆면, 아랫면, 테두리의 색

GRAVITY = 1

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

aquire_piece_count = 0
texture_num = 0
warp_working_count = 0

#색칠 변수
color = 0

#키 누름 카운트
z_key_count =0

#블록 설치
blocks = []

