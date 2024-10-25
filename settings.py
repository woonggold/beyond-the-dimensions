import pygame    
pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

camera_pos = [0, 0, -1000]
camera_speed = 10  # 카메라 이동 속도
is_3D = False
target_camera_pos = camera_pos # 목표 카메라 위치

angle_x, angle_y = 0, 0

map_name = "test"#이 map name을 변경해서 맵을 변경할 수 있음

mouse_sensitivity = 0.003

cube_size = 50

class Showing():
    def __init__(self):
        self.squares_front = []
        self.squares = []

showing = Showing()