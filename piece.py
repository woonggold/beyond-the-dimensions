import pygame
import math
import os
import projection_3D
from settings import *
from player import *
script_dir = os.path.dirname(__file__)

class MakePiece:
    def __init__(self, pos, event, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.original_z = pos[2]
        self.size = size

        self.img = pygame.image.load(f"{script_dir}//images//차원조각.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.width, self.height = self.rect.width,self.rect.height
        self.display = True
        self.event = event # 무슨 이벤트가 일어나게 할지 이벤트 명 적기


Pieces = []
#def load_piece
#   return Pieces

def draw_real_piece():
    import real_game
    for piece in Pieces:
        if piece.display == False:
            return
        aquire_piece_check(piece)
        x, y, z = piece.x, piece.y, piece.z
        dx = abs(x-real_game.camera_pos[0])
        dy = abs(y-real_game.camera_pos[1])
        dz = abs(z-real_game.camera_pos[2])
        piece_range = (dx**2+dy**2+dz**2)**(1/2)
        result = projection_3D.project_3d_or_2d((x,y,z), real_game.camera_pos,real_game.angle_x,real_game.angle_y)
        modified_img = pygame.transform.scale(piece.img, (piece.size * 200*piece.width / piece_range, piece.size * 200*piece.height / piece_range))
        modified_rect = modified_img.get_rect()
        modified_width, modified_height = modified_rect.width, modified_rect.height 
        if result != None:
            screen.blit(modified_img, (result[0] - (modified_width / 2), result[1] - (modified_height / 2)))

def aquire_piece_check(piece):
    global Pieces
    if abs(player.x - piece.x) < 100 and 200 > player.y - piece.y > -100 and abs(player.z - piece.z) < 50:
        Pieces.remove(piece)
        piece_event_check(piece.event)

def piece_event_check(event):
    import real_game, map_loading
    match event:
        case "2D":
            real_game.is_3D = False
        case "3D":
            temp = []
            for block in map_loading.BLOCKS:
                if abs(block.x - player.x) < 100:
                    temp.append(block.original_z)
            if not temp:
                player.z = 100
            else: 
                player.z = min(temp)
            real_game.is_3D = True
        case "2":
            print('2')
        case "3":
            print('3')

def piece_3D_transition():
    import real_game
    
    # 부드럽게 이동
    for piece in Pieces:
        if real_game.is_3D == False: #2D
            if(abs(100 - piece.z)>10):
                piece.z += (100 - piece.z) * 0.3
            else:
                piece.z = 100

        else: #3D
            if(abs(piece.original_z - piece.z)>10):
                piece.z += (piece.original_z - piece.z) * 0.3
            else:
                piece.z = piece.original_z
