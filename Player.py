import pygame
import math
import os

script_dir = os.path.dirname(__file__)

class Player:
    def __init__(self, pos, image):
        self.pos = pos
        self.x ,self.y, self.z = pos
        self.image = f"{script_dir}//images//{image}"