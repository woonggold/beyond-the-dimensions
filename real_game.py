import pygame
import math

# 파이게임 초기화
def reset():
    global screen_height,screen_width,screen,clock,camera_pos,camera_speed,is_topdown_view,target_camera_pos,cube_size,\
    cube_pos,floor_points,BLOCKS,angle_x,angle_y,mouse_sensitivity
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # 카메라 및 게임 상태 변수
    camera_pos = [0, 0, -1000]  # 카메라 초기 위치 (플랫포머뷰)
    camera_speed = 10  # 카메라 이동 속도
    is_topdown_view = False  # 시점 전환 플래그 (False: 플랫포머뷰, True: 탑뷰)
    target_camera_pos = camera_pos[:]  # 목표 카메라 위치

    # 큐브의 기본 좌표
    cube_size = 50  # 큐브의 크기
    cube_pos = [0, -cube_size, 25]  # 큐브의 위치 (바닥 높이에 맞춰 조정)


    # 바닥의 좌표 (길고 넓은 직사각형)
    floor_points = [
        (-400, 0, -800), (400, 0, -800),
        (400, 0, -1000), (-400, 0, -1000)
    ]
    BLOCKS = []
    for i in range(10):
        for j in range(10):
            BLOCKS.append(Block((i*100-500,500,j*100-500),50))

    angle_x, angle_y = 0, 0

# 마우스 감도 설정
    mouse_sensitivity = 0.001

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


# 3D 좌표를 2D 화면에 투영하는 함수
    def project_3d_to_2d(self, camera_pos):
        result =[]
        #point[2] = ㄹㅇ 블럭좌표
        #point[3] = 부드러운 전환을 위해 필요
        #z = 최종 계산에 쓰이는 값
        for point in self.points:
            # x,y,self.z2 = pos
            if is_topdown_view == False:
                x, y = point[0],point[1]
                # camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1
                point[3] += (50 - point[3]) * 0.2
                z = point[3]
            else:
                x, y = point[0],point[1]
                point[3] += (point[2] - point[3]) * 0.2
                z = point[3]

            x -= camera_pos[0]
            y -= camera_pos[1]
            z -= camera_pos[2]

            # 원근 투영 적용
            camera_distance = 500
            x,y,z = rotate_point((x,y,z),angle_x,angle_y)

            if z <= -camera_distance+0.00001:  # 너무 가까운 z 좌표는 렌더링하지 않음
                result.append(None)
            else:
                factor = camera_distance / (camera_distance + z)
                x_2d = x * factor + screen_width/2 # 화면 중앙으로 이동
                y_2d = y * factor + screen_height/2  # 화면 중앙으로 이동
                result.append((int(x_2d), int(y_2d)))
        return result


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.x ,self.y, self.z = pos



def rotate_point(point, angle_x, angle_y):
    """3D 점을 주어진 각도만큼 회전시킨 좌표를 반환"""
    x, y, z = point
    angle_x = angle_x
    angle_y = -angle_y

    # y축 회전
    cos_theta = math.cos(angle_y)
    sin_theta = math.sin(angle_y)
    x, z = cos_theta * x + sin_theta * z, -sin_theta * x + cos_theta * z

    # x축 회전
    cos_theta = math.cos(angle_x)
    sin_theta = math.sin(angle_x)
    y, z = cos_theta * y - sin_theta * z, sin_theta * y + cos_theta * z

    return [x, y, z]

def draw_line(one,two):
    if all((one,two)):
        pygame.draw.line(screen, (255, 255, 255), one, two, 1)
# 큐브의 면을 그리는 함수
def draw_cube(points):
    # 앞면
    draw_line(points[0], points[1])
    draw_line(points[1], points[2])
    draw_line(points[2], points[3])
    draw_line(points[3], points[0])

    if is_topdown_view:
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

def run(reseted):
    global is_topdown_view,target_camera_pos,cube_pos,camera_pos,angle_x,angle_y
    condition = "real_game"
    if reseted == True:
        pass
    else:
        reset()
        print(2)
        reseted = True
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # 각도 업데이트 (마우스 이동에 따라)
    angle_y += mouse_dx * mouse_sensitivity
    angle_x += mouse_dy * mouse_sensitivity

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition =  "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                condition =  "quit"  # 스페이스바를 눌렀을 때
            if event.key == pygame.K_SPACE:
                # 시점 전환 목표 설정
                is_topdown_view = not is_topdown_view
                if is_topdown_view:
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

    # 키 입력 처리 (3D 뷰에서도 큐브 이동)
    keys = pygame.key.get_pressed()
    if is_topdown_view:
        if keys[pygame.K_a]:
            cube_pos[0] -= camera_speed  # 3D에서 큐브를 왼쪽으로 이동
        if keys[pygame.K_d]:
            cube_pos[0] += camera_speed  # 3D에서 큐브를 오른쪽으로 이동
    else:
        if keys[pygame.K_a]:
            cube_pos[0] -= camera_speed  # 플랫포머뷰에서 큐브를 왼쪽으로 이동
        if keys[pygame.K_d]:
            cube_pos[0] += camera_speed  # 플랫포머뷰에서 큐브를 오른쪽으로 이동

    # 카메라 부드럽게 이동
    for i in range(3):
        camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1  # 보간값을 조정하여 부드럽게 이동

    screen.fill((0, 0, 0))

    for block in BLOCKS:
        draw_cube(block.project_3d_to_2d(camera_pos))

    pygame.display.flip()
    clock.tick(60)
    return [condition,reseted]