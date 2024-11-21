import pygame
from pygame.locals import *
from settings import *
from moviepy.editor import *
import map_loading
import time
import settings
import importlib
from settings import *
import dialogue
from dialogue import *
import map_loading
from map_loading import *
import real_game
from real_game import *
import ending
from ending import *
import piece
from piece import *
import dead
from dead import *
import pattern
from pattern import *
clip = VideoFileClip(f"{script_dir}//videos//start_video.mp4")


def run():
    esc_start = 0
    esc_timer = 0
    importlib.reload(piece)
    importlib.reload(real_game)
    importlib.reload(dialogue)
    importlib.reload(ending)
    importlib.reload(dead)
    importlib.reload(pattern)
    importlib.reload(settings)
    pygame.mixer.music.stop()
    importlib.reload(map_loading)
    map_loading.map_load("stage1")
    
    pygame.display.set_caption('Beyond the Dimensions')
    font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 20)
    skip_text = font.render('좌클릭으로 영상 스킵', True, (128, 128, 128))
    pygame.mixer.music.load(f"{script_dir}//music//noise.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    for frame in clip.iter_frames(fps=24, dtype="uint8"):
        stopped = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.mixer.music.stop()
                stopped = 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if esc_timer == 0:
                esc_start = time.time()
            esc_timer = time.time() - esc_start + 0.01
            if esc_timer >= 1:
                pygame.mixer.music.stop()
                map_loading.map_load("stage1")
                return "real_game"
        else:
            esc_timer = 0
        if stopped:
            break
                
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        proportion = screen_width / frame_surface.get_rect().width
        modified_height = frame_surface.get_rect().height * screen_width / frame_surface.get_rect().width
        margin = (screen_height - modified_height) / 2
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, int(modified_height)))
        screen.fill((0, 0, 0))
        screen.blit(frame_surface, (0, margin))
        screen.blit(skip_text, (screen_width - 200, 10))
        pygame.display.update()
        clock.tick(24)
    
    return "real_game"