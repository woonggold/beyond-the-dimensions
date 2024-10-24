import math
import pygame
from settings import *


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



def project_3d_or_2d(points, camera_pos,is_3D,angle_y,angle_x):
        result =[]
        #point[2] = ㄹㅇ 블럭좌표
        #point[3] = 부드러운 전환을 위해 필요
        #z = 최종 계산에 쓰이는 값
        for point in points:
            # x,y,self.z2 = pos
            if is_3D == False:
                x, y = point[0],point[1]
                # camera_pos[i] += (target_camera_pos[i] - camera_pos[i]) * 0.1
                if(abs(100 - point[3])>10):
                    point[3] += (100 - point[3]) * 0.2
                else:
                    point[3] = 100
                z = point[3]
            else:
                x, y = point[0],point[1]
                if(abs(point[2] - point[3])>10):
                    point[3] += (point[2] - point[3]) * 0.2
                else:
                    point[3] = point[2]
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