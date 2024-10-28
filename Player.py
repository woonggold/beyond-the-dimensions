import pygame
import math
import os
import real_game
from settings import *
script_dir = os.path.dirname(__file__)

class Player:
    def __init__(self, pos, image):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.fake_x = self.x
        self.fake_z = self.z
        self.size = 50
        self.points = [
            [self.x - self.size, self.y - 3*self.size], [self.x + self.size, self.y - 3*self.size],
            [self.x + self.size, self.y + self.size], [self.x - self.size, self.y + self.size],
        ]
        self.border = [[50,-50],[50,-150],[1,-1]]
        self.image = f"{script_dir}//images//{image}"
        self.dx, self.dy, self.dz = [0,0,0]
        self.jump_OK = False
        self.range = 0
        self.jump_power = -20
        self.ani = "stand"
        self.speed = 18
        self.jump_pressed = False
player = Player((100,0,-500),"player.png")

