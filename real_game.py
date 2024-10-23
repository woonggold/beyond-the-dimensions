import pygame
import math
import projection_3D
# 파이게임 초기화
def reset():
    global screen_height,screen_width,screen,clock,camera_pos,camera_speed,is_3D,target_camera_pos,cube_size,\
    cube_pos,floor_points,BLOCKS,angle_x,angle_y,mouse_sensitivity
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # 카메라 및 게임 상태 변수
    camera_pos = [0, 0, -1000]  # 카메라 초기 위치 (플랫포머뷰)
    camera_speed = 10  # 카메라 이동 속도
    is_3D = False  # 시점 전환 플래그 (False: 플랫포머뷰, True: 탑뷰)
    target_camera_pos = camera_pos # 목표 카메라 위치

    cube_size = 50  # 큐브의 크기

    BLOCKS = []
    for i in range(10):
        for j in range(10):
            BLOCKS.append(Block((i*100-500,500,j*100-500),cube_size))

    angle_x, angle_y = 0, 0

# 마우스 감도 설정
    mouse_sensitivity = 0.003

# 마우스 중앙 고정
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

class Block:
    def __init__(self, pos, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = size
        self.points = [
            [self.x - self.size, self.y - self.size, self.z - self.size, self.z - self.size], [self.x + self.size, self.y - self.size, self.z - self.size, self.z - self.size],
            [self.x + self.size, self.y + self.size, self.z - self.size, self.z - self.size], [self.x - self.size, self.y + self.size, self.z - self.size, self.z - self.size],
            [self.x - self.size, self.y - self.size, self.z + self.size, self.z + self.size], [self.x + self.size, self.y - self.size, self.z + self.size, self.z + self.size],
            [self.x + self.size, self.y + self.size, self.z + self.size, self.z + self.size], [self.x - self.size, self.y + self.size, self.z + self.size, self.z + self.size]
        ]
# 큐브의 8개 꼭짓점 좌표 생성 함수


def draw_line(one,two):
    if all((one,two)):
        pygame.draw.line(screen, (0, 0, 0), one, two, 1)
# 큐브의 면을 그리는 함수
def draw_cube(points):
    # 앞면
    draw_line(points[0], points[1])
    draw_line(points[1], points[2])
    draw_line(points[2], points[3])
    draw_line(points[3], points[0])

    if is_3D:
        # 뒷면
        draw_line(points[4], points[5])
        draw_line(points[5], points[6])
        draw_line(points[6], points[7])
        draw_line(points[7], points[4])

        # 앞면과 뒷면을 연결하는 선들
        draw_line(points[0], points[4])
        draw_line(points[1], points[5])
        draw_line(points[2], points[6])
        draw_line(points[3], points[7])

# 바닥 그리기 함수
# def draw_floor(camera_pos):
#     floor_projected = [project_3d_to_2d(point, camera_pos) for point in floor_points]
    
#     if None not in floor_projected:
#         pygame.draw.polygon(screen, (100, 100, 100), floor_projected)  # 바닥을 그린다

# 메인 루프
def mouse_rotate_check():
    global angle_x, angle_y
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # 각도 업데이트 (마우스 이동에 따라)
    angle_y += mouse_dx * mouse_sensitivity
    angle_x += mouse_dy * mouse_sensitivity

def event_check():
    global condition, is_3D, target_camera_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition =  "quit"
            if event.key == pygame.K_SPACE:
                # 시점 전환 목표 설정
                is_3D = not is_3D
                if is_3D:
                    # target_camera_pos[0] = 0  # 탑뷰 카메라 위치 설정
                    target_camera_pos[1] -= 250
                    target_camera_pos[2] -= 250 # 바닥이 보이도록 카메라 높이 조정
                else:
                    # target_camera_pos[0] = 0  # 플랫포머뷰 카메라 위치 설정
                    target_camera_pos[1] += 250
                    target_camera_pos[2] += 250
        

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 휠 클릭을 감지
            if event.button == 4:  # 휠을 위로 스크롤
                target_camera_pos[2] += camera_speed * 2  # 카메라를 앞으로 이동
            elif event.button == 5:  # 휠을 아래로 스크롤
                target_camera_pos[2] -= camera_speed * 2  # 카메라를 뒤로 이동

def camera_move():
    # 부드럽게 이동
    global camera_pos
    for i in range(3):
        camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1

def draw_screen():
    screen.fill((255, 255, 255))

    for block in BLOCKS:
        draw_cube(projection_3D.project_3d_or_2d(block.points,camera_pos,is_3D,angle_x,angle_y))
    pygame.display.flip()
    clock.tick(60)

def run():
    global condition
    condition = "real_game"
    mouse_rotate_check()
    event_check()
    camera_move()
    draw_screen()
    return condition