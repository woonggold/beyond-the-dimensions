import pygame
import math

# 파이게임 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 카메라 및 게임 상태 변수
camera_pos = [0, 0, -1000]  # 카메라 초기 위치 (플랫포머뷰)
camera_speed = 10  # 카메라 이동 속도
is_topdown_view = False  # 시점 전환 플래그 (False: 플랫포머뷰, True: 탑뷰)
target_camera_pos = camera_pos[:]  # 목표 카메라 위치

# 큐브의 기본 좌표
cube_pos = [0, 0, 0]  # 큐브의 위치
cube_size = 100  # 큐브의 크기

# 큐브의 8개 꼭짓점 좌표 생성 함수
def get_cube_points(cube_pos, size):
    x, y, z = cube_pos
    points = [
        (x - size, y - size, z - size), (x + size, y - size, z - size),
        (x + size, y + size, z - size), (x - size, y + size, z - size),
        (x - size, y - size, z + size), (x + size, y - size, z + size),
        (x + size, y + size, z + size), (x - size, y + size, z + size)
    ]
    return points

# 3D 좌표를 2D 화면에 투영하는 함수
def project_3d_to_2d(point, camera_pos):
    x, y, z = point
    x -= camera_pos[0]
    y -= camera_pos[1]
    z -= camera_pos[2]

    # 원근 투영 적용
    camera_distance = 500
    if z <= 0.000001:  # 너무 가까운 z 좌표는 렌더링하지 않음
        return None

    factor = camera_distance / (camera_distance + z)
    x_2d = x * factor + 400  # 화면 중앙으로 이동
    y_2d = y * factor + 300  # 화면 중앙으로 이동
    return (int(x_2d), int(y_2d))

# 큐브의 면을 그리는 함수
def draw_cube(points):
    # 앞면
    pygame.draw.line(screen, (255, 255, 255), points[0], points[1], 2)
    pygame.draw.line(screen, (255, 255, 255), points[1], points[2], 2)
    pygame.draw.line(screen, (255, 255, 255), points[2], points[3], 2)
    pygame.draw.line(screen, (255, 255, 255), points[3], points[0], 2)

    if is_topdown_view:
        # 뒷면
        pygame.draw.line(screen, (255, 255, 255), points[4], points[5], 2)
        pygame.draw.line(screen, (255, 255, 255), points[5], points[6], 2)
        pygame.draw.line(screen, (255, 255, 255), points[6], points[7], 2)
        pygame.draw.line(screen, (255, 255, 255), points[7], points[4], 2)

        # 앞면과 뒷면을 연결하는 선들
        pygame.draw.line(screen, (255, 255, 255), points[0], points[4], 2)
        pygame.draw.line(screen, (255, 255, 255), points[1], points[5], 2)
        pygame.draw.line(screen, (255, 255, 255), points[2], points[6], 2)
        pygame.draw.line(screen, (255, 255, 255), points[3], points[7], 2)

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # 스페이스바를 눌렀을 때
            if event.key == pygame.K_SPACE:
                # 시점 전환 목표 설정
                is_topdown_view = not is_topdown_view
                if is_topdown_view:
                    target_camera_pos[0] = 0  # 탑뷰 카메라 위치 설정
                    target_camera_pos[1] = -500
                    target_camera_pos[2] = -1000
                else:
                    target_camera_pos[0] = 0  # 플랫포머뷰 카메라 위치 설정
                    target_camera_pos[1] = 0
                    target_camera_pos[2] = -1000
        

    # 키 입력 처리 (플랫포머뷰에서만 큐브 이동)
    keys = pygame.key.get_pressed()
    if not is_topdown_view:
        if keys[pygame.K_a]:
            cube_pos[0] -= camera_speed
        if keys[pygame.K_d]:
            cube_pos[0] += camera_speed

    # 카메라 부드럽게 이동
    for i in range(3):
        camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1  # 보간값을 조정하여 부드럽게 이동

    screen.fill((0, 0, 0))

    # 큐브 좌표 생성 및 투영
    cube_points = get_cube_points(cube_pos, cube_size)
    projected_cube = [project_3d_to_2d(point, camera_pos) for point in cube_points]

    # 큐브 그리기
    if None not in projected_cube:
        draw_cube(projected_cube)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
