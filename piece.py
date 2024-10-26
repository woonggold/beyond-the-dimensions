import pygame
import math
import os
import projection_3D  # projection_3D를 import하여 투영 함수 사용
script_dir = os.path.dirname(__file__)

class MakePiece:
    def __init__(self, pos, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = size
        self.points = [
            (self.x + self.size, self.y + self.size, self.z),
            (self.x - self.size, self.y + self.size, self.z),
            (self.x - self.size, self.y - self.size, self.z), 
            (self.x + self.size, self.y - self.size, self.z), 
        ]
        

    # def update_points(self, camera_pos, angle_x, angle_y):
    #     # 카메라 위치와 앵글을 사용하여 3D 투영 계산
    #     self.projected_points = projection_3D.project_3d_or_2d_for_piece(self.points, camera_pos, angle_x, angle_y)

pieceblock = MakePiece((0,175,-500), 50)
