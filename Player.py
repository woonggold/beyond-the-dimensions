import pygame
import math
import os
import real_game
script_dir = os.path.dirname(__file__)

class Player:
    def __init__(self, pos, image):
        self.pos = pos
        self.x ,self.y, self.z = pos
        self.image = f"{script_dir}//images//{image}"

class PLAYBlock:
    def __init__(self, pos, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = size
        self.points = [
            [self.x - self.size, 2*(self.y - self.size), self.z - self.size, self.z - self.size], [self.x + self.size, 2 *(self.y - self.size), self.z - self.size, self.z - self.size],
            [self.x + self.size, 2*(self.y + self.size), self.z - self.size, self.z - self.size], [self.x - self.size, 2 *(self.y + self.size), self.z - self.size, self.z - self.size],
            [self.x - self.size, 2*(self.y - self.size), self.z + self.size, self.z + self.size], [self.x + self.size, 2 *(self.y - self.size), self.z + self.size, self.z + self.size],
            [self.x + self.size, 2*(self.y + self.size), self.z + self.size, self.z + self.size], [self.x - self.size, 2 *(self.y + self.size), self.z + self.size, self.z + self.size]
        ]
playerblock = PLAYBlock((0,175,-500),50)
