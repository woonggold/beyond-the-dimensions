import moderngl
import pygame
import numpy as np
from pygame.locals import *

# Pygame 초기화
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# ModernGL 컨텍스트 생성
ctx = moderngl.create_context()

# 버텍스 셰이더와 프래그먼트 셰이더 정의
vertex_shader = '''
    #version 330
    in vec3 in_vert;
    uniform mat4 model;
    uniform mat4 projection;
    void main() {
        gl_Position = projection * model * vec4(in_vert, 1.0);
    }
'''
fragment_shader = '''
    #version 330
    out vec4 f_color;
    void main() {
        f_color = vec4(0.3, 0.5, 0.8, 1.0);
    }
'''

# 프로그램 생성
prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

# 큐브 정점 정의
define_cube_vertices = [
    -1, -1, -1,  1, -1, -1,  1,  1, -1,  -1,  1, -1,  # 뒷면
    -1, -1,  1,  1, -1,  1,  1,  1,  1,  -1,  1,  1   # 앞면
]
vertices = np.array(define_cube_vertices, dtype='f4')
vbo = ctx.buffer(vertices.tobytes())

vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

# 투영 행렬 및 변환 행렬 정의
def perspective(fovy, aspect, near, far):
    f = 1.0 / np.tan(fovy / 2.0)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype='f4')

proj = perspective(np.radians(45.0), display[0] / display[1], 0.1, 100.0)
model = np.eye(4, dtype='f4')

# 셰이더 프로그램에 행렬 설정
prog['projection'].write(proj.tobytes())

# 게임 루프
running = True
angle = 0.0
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # 화면 지우기
    ctx.clear(0.9, 0.9, 0.9)

    # 회전 변환 설정
    angle += 0.01
    cos_theta, sin_theta = np.cos(angle), np.sin(angle)
    model[0, 0] = cos_theta
    model[0, 2] = sin_theta
    model[2, 0] = -sin_theta
    model[2, 2] = cos_theta
    prog['model'].write(model.tobytes())

    # 큐브 그리기
    vao.render(moderngl.TRIANGLE_FAN)

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
