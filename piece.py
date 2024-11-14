import pygame
import math
import os
import projection_3D
from settings import *
from player import *
import real_game
script_dir = os.path.dirname(__file__)
core_hp = 500
core_in = False
extend_modified_size = 0

class MakePiece:
    def __init__(self, pos, event, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.original_z = pos[2]
        self.size = int(size)
        self.img = pygame.image.load(f"{script_dir}//images//차원조각.png").convert_alpha()
        if event == "core":
            self.img = pygame.image.load(f"{script_dir}//images//에너지코어.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.width, self.height = self.rect.width,self.rect.height
        self.display = True
        self.event = event # 무슨 이벤트가 일어나게 할지 이벤트 명 적기
        self.range = 1
        self.drawed = False



Pieces = []
#def load_piece
#   return Pieces
def cal_range():
    import real_game
    for piece in Pieces:
        x, y, z = piece.x, piece.y, piece.z
        dx = abs(x-real_game.camera_pos[0])
        dy = abs(y-real_game.camera_pos[1])
        dz = abs(z-real_game.camera_pos[2])
        piece.range = (dx**2+dy**2+dz**2)

def draw_real_piece(range):
    for piece in Pieces:
        if piece.display == False:
            return
        
        if piece.range > range and piece.drawed == False:
            forced_draw(piece)
            
def forced_draw(piece):
    import real_game
    piece.drawed = True
    aquire_piece_check(piece)
    result = projection_3D.project_3d_or_2d((piece.x, piece.y, piece.z), real_game.camera_pos, real_game.angle_x, real_game.angle_y)

    # 크기 제한 설정
    
    modified_size = int(piece.size * 200 * piece.width / (piece.range**(1/2)))
    if modified_size > 10000:
        modified_size = 10000
    modified_img = pygame.transform.scale(piece.img, (modified_size,modified_size))
    modified_rect = modified_img.get_rect()
    modified_width, modified_height = modified_rect.width, modified_rect.height
    if result:
        screen.blit(modified_img, (result[0] - (modified_width / 2), result[1] - (modified_height / 2)))


def aquire_piece_check(piece):
    global Pieces,core_in
    if abs(player.x - piece.x) < 100 and 200 > player.y - piece.y > -100 and abs(player.z - piece.z) < 50 and piece.event != "core":
        piece_event_check(piece.event)
        if piece.event not in ["stage_per1","stage_per2"]:
            Pieces.remove(piece)
    if piece.event == "core":
        core_in = False
        if abs(player.x - piece.x) < 200 and 300 > player.y - piece.y > -200 and abs(player.z - piece.z) < 150:
            core_in = True

def piece_event_check(event):
    global extend_piece_pos, extend_modified_size
    import real_game, map_loading, settings
    # print (real_game.scr_effect)
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
        case "normal":
            settings.scr_effect = "normal"
        case "rotate":
            settings.scr_effect = "rotate"
        case "rotater":
            settings.scr_effect = "rotater"
        case "rotatel":
            settings.scr_effect = "rotatel"
        case "rotating":
            import time
            global rotate_start
            rotate_start = time.time()
            settings.scr_effect = "rotating"
        case "block_disappear":
            real_game.m_key_count = 1
            real_game.last_update = pygame.time.get_ticks()
            real_game.reset_block_timers()
            print("m 키 눌림 - 타이머 시작")   
        case "block_disappear_break":
            real_game.m_key_count = 0
        case "extend":
            real_game.extend_piece = True
            for piece in Pieces:
                if piece.event == "stage7":
                    extend_piece_pos = projection_3D.project_3d_or_2d((piece.x, piece.y, piece.z), real_game.camera_pos, real_game.angle_x, real_game.angle_y)
                    extend_modified_size = int(piece.size * 200 * piece.width / (piece.range**(1/2)))
        case "stage":
            for piece in Pieces:
                if piece.event == "stage":
                    player.x,player.y,player.z = piece.x,piece.y+100,piece.z
        case "stage_per1":
            for piece in Pieces:
                if piece.event == "stage_per1":
                    player.y = piece.y+100
                    player.jump_pressed = False
        case "stage_per2":
            for piece in Pieces:
                if piece.event == "stage_per2":
                    player.y = piece.y+100
                    player.jump_pressed = False




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
